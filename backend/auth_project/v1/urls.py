from django.urls import path
from v1.rest_api import register, login, account

urlpatterns = [
    # Email verification
    path("send-otp", account.SendOtpToMail.as_view(), name="send-otp"),
    path("verify-otp", account.VerifyOtp.as_view(), name="verify-otp"),
    # User registration
    path("register", register.UserRegister.as_view(), name="register"),
    # Login
    path("login", login.Login.as_view(), name="login"),
    # Forgot password
    path("forgot-password", account.ForgotPassword.as_view(), name="forgot-password"),
]
