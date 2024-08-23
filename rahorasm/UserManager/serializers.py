from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class OTPValidateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

class SignupSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)
    name = serializers.CharField(max_length=100)