from django.urls import path
from .views import ContactUsView, LoginView, LoginRequestOTPView, LoginValidateOTPView, SignupRequestView, SignupValidateOTPView, UserSessionView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('login/request', LoginRequestOTPView.as_view(), name='login_request_otp'),
    path('login/validate', LoginValidateOTPView.as_view(), name='login_validate_otp'),
    path('signup/request', SignupRequestView.as_view(), name='signup_request'),
    path('signup/validate', SignupValidateOTPView.as_view(), name='signup_validate_otp'),
    path('user-session', UserSessionView.as_view(), name='user_session'),
    path('contact-us', ContactUsView.as_view(), name='contact_us')
]