from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, OTPRequestSerializer, OTPValidateSerializer, SignupSerializer, ContactUsSerializer
from django.contrib.auth import authenticate, login
from django.core.cache import cache
import random
from .utils import send_otp
from .models import UserModel as User, ContactForm
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):      
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response({"message": "با موفقیت وارد شدید"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "حساب کاربری شما فعال نیست"}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message": "شماره تلفن و یا گذرواژه اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginRequestOTPView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            # Check if the user exists in the database
            user_exists = User.objects.filter(phone_number=phone_number).exists()
            if not user_exists:
                return Response({"message": "کاربری با این شماره تلفن وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
            
            # Check if an OTP was generated in the last 60 seconds
            if cache.get(f"otp_cooldown_{phone_number}"):
                return Response({"message": "کد یکبار مصرف به تازگی ارسال شده لطفا چند دقیقه دیگر مجددا تلاش نمایید"}, 
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store OTP in cache with 5 minutes expiration
            cache.set(f"otp_{phone_number}", otp, 300)
            
            # Set cooldown
            cache.set(f"otp_cooldown_{phone_number}", True, 60)
            print(otp)
            send_otp(phone_number, otp)
            
            return Response({"message": "کد یکبار مصرف با موفقیت ارسال شد"}, status=status.HTTP_200_OK)
        return Response({'message': 'اطلاعات وارد شده صحیح نمی باشد'}, status=status.HTTP_400_BAD_REQUEST)

class LoginValidateOTPView(APIView):
    def post(self, request):
        serializer = OTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            
            stored_otp = cache.get(f"otp_{phone_number}")
            
            if stored_otp and stored_otp == otp:
                cache.delete(f"otp_{phone_number}")
                user = User.objects.get(phone_number=phone_number)
                login(request, user)
                return Response({"message": "OTP validated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignupRequestView(APIView):
    def post(self, request):
        if not request.data:
            return Response({"message": "لطفا فیلد ها را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            # Store user data temporarily
            cache.set(f"signup_{serializer.validated_data['phone_number']}", serializer.validated_data, 300)
            
            phone_number = serializer.validated_data['phone_number']
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store OTP in cache with 5 minutes expiration
            cache.set(f"otp_{phone_number}", otp, 300)
            
            # Set cooldown
            cache.set(f"otp_cooldown_{phone_number}", True, 60)
            print(otp)
            # send_otp(phone_number, otp)
            
            return Response({"message": "کد یکبار مصرف ارسال شد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignupValidateOTPView(APIView):
    def post(self, request):
        serializer = OTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            
            stored_otp = cache.get(f"otp_{phone_number}")
            user_data = cache.get(f"signup_{phone_number}")
            
            if stored_otp and stored_otp == otp and user_data:
                # Create user
                user = User.objects.create_user(phone_number=phone_number, password=user_data['password'])
                user.name = user_data['name']
                user.save()
                
                cache.delete(f"otp_{phone_number}")
                cache.delete(f"signup_{phone_number}")
                login(request, user)
                
                return Response({"message": "کاربر با موفقیت ایجاد شد"}, status=status.HTTP_201_CREATED)
            return Response({"message": "کد را به درستی وارد نکرده اید."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "اطلاعات به درستی ارسال نشده است"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserSessionView(APIView):

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            session_data = None
            return Response({'payload': session_data})
        else:
            session_data = {
                'id': user.id,
                'name': user.name,
                'phone_number': user.phone_number,
                'email': user.email,
                'is_staff': user.is_staff,
            }
            return Response({"payload": session_data}, status=status.HTTP_200_OK)
        
        
class ContactUsView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactUsSerializer