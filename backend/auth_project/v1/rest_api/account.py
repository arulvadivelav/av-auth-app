import pytz

from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta

from auth_project.settings import EMAIL_HOST_USER, OTP_EXPIRY_TIME, OTP_LENGTH
from v1.models import EmailVerification
from v1.serializers.register import ForgotSerializer, OtpSerializer
from v1.utils.basic_utils import generate_otp, mail_content
from v1.utils.response_util import common_response_format
from v1.constants.constants import (
    RESPONSE_CODE_200,
    RESPONSE_CODE_400,
    RESPONSE_CODE_500,
    HTTP_RESPONSE_STATUS_200,
    HTTP_RESPONSE_STATUS_400,
    HTTP_RESPONSE_STATUS_500,
)


class SendOtpToMail(APIView):
    """This endpoint is used to send a OTP to the given email to verify the email id."""

    def post(self, request):
        try:
            serializer = OtpSerializer(data=request.data)
            if serializer.is_valid():
                mail_id = serializer.validated_data["email_id"]
                # OTP generation
                (
                    otp_status,
                    otp_msg,
                    otp,
                ) = generate_otp(OTP_LENGTH)
                if not otp_status:
                    return common_response_format(
                        False,
                        [],
                        otp_msg,
                        RESPONSE_CODE_400,
                        HTTP_RESPONSE_STATUS_400,
                    )
                # Check existing user
                user_ref = EmailVerification.objects.filter(email=mail_id)
                if user_ref:
                    user_ref.update(otp=otp, updated_at=datetime.now(pytz.UTC))
                    return common_response_format(
                        True,
                        [],
                        "Otp sent to your email address.",
                        RESPONSE_CODE_200,
                        HTTP_RESPONSE_STATUS_200,
                    )
                else:
                    # Draft a new Mail content
                    subject, content = mail_content(otp)
                    email = EmailMessage(
                        subject=subject,
                        body=content,
                        from_email=EMAIL_HOST_USER,
                        to=[mail_id],
                    )
                    email.send()

                    # Create a new user mail details to verify the otp.
                    if email:
                        EmailVerification.objects.create(email=mail_id, otp=otp)
                    return common_response_format(
                        True,
                        [],
                        "Otp sent to your email address.",
                        RESPONSE_CODE_200,
                        HTTP_RESPONSE_STATUS_200,
                    )
            else:
                return common_response_format(
                    False,
                    [],
                    serializer.errors,
                    RESPONSE_CODE_400,
                    HTTP_RESPONSE_STATUS_400,
                )

        except Exception as e:
            return common_response_format(
                False,
                [],
                "Internal server error. Please try again later...",
                RESPONSE_CODE_500,
                HTTP_RESPONSE_STATUS_500,
            )


class VerifyOtp(APIView):
    """This endpoint is used to verify the OTP with the mail."""

    def post(self, request):
        try:
            try:
                email_id = str(request.data["email_id"])
                otp = str(request.data["otp"])
            except:
                return common_response_format(
                    False,
                    [],
                    "Required fields are missing.",
                    RESPONSE_CODE_400,
                    HTTP_RESPONSE_STATUS_400,
                )
            # Check OTP length
            if len(otp) > OTP_LENGTH:
                return common_response_format(
                    False,
                    [],
                    f"Invalid OTP. The OTP length should be {OTP_LENGTH} characters long.",
                    RESPONSE_CODE_400,
                    HTTP_RESPONSE_STATUS_400,
                )
            # Verify OTP
            try:
                verify_mail = EmailVerification.objects.get(email=email_id, otp=otp)
            except:
                return common_response_format(
                    False,
                    [],
                    "Invalid OTP.",
                    RESPONSE_CODE_400,
                    HTTP_RESPONSE_STATUS_400,
                )
            if verify_mail:
                otp_expiry_time = verify_mail.updated_at + timedelta(
                    minutes=OTP_EXPIRY_TIME
                )
                # Check OTP expiry time
                UTC_TIME_NOW = datetime.now(pytz.UTC)
                if UTC_TIME_NOW > otp_expiry_time:
                    return common_response_format(
                        False,
                        [],
                        "OTP expired.",
                        RESPONSE_CODE_400,
                        HTTP_RESPONSE_STATUS_400,
                    )

                # If OTP not expired
                verify_mail.verified = True
                verify_mail.save()
                return common_response_format(
                    True,
                    [],
                    "OTP verified successfully",
                    RESPONSE_CODE_200,
                    HTTP_RESPONSE_STATUS_200,
                )
            else:
                return common_response_format(
                    False,
                    [],
                    "Invalid OTP.",
                    RESPONSE_CODE_400,
                    HTTP_RESPONSE_STATUS_400,
                )
        except Exception as e:
            return common_response_format(
                False,
                [],
                "Internal server error. Please try again later...",
                RESPONSE_CODE_500,
                HTTP_RESPONSE_STATUS_500,
            )


class ForgotPassword(APIView):
    """This endpoint is used to forgot/reset password with the OTP received in email."""

    def post(self, request):
        try:
            serializer = ForgotSerializer(data=request.data)
            if serializer.is_valid():
                valid_data = serializer.validated_data
                email_id = valid_data["email_id"]
                otp = valid_data["otp"]
                password = valid_data["new_password"]

                # Check user details found for the given mail id
                user_ref = User.objects.filter(email=email_id).first()
                if not user_ref:
                    return common_response_format(
                        False,
                        [],
                        "User details not found for the email.",
                        RESPONSE_CODE_400,
                        HTTP_RESPONSE_STATUS_400,
                    )
                # Verify OTP
                try:
                    verify_mail = EmailVerification.objects.get(email=email_id, otp=otp)
                except:
                    return common_response_format(
                        False,
                        [],
                        "Invalid OTP.",
                        RESPONSE_CODE_400,
                        HTTP_RESPONSE_STATUS_400,
                    )

                # Check OTP expiry time
                if verify_mail:
                    otp_expiry_time = verify_mail.updated_at + timedelta(
                        minutes=OTP_EXPIRY_TIME
                    )
                    UTC_TIME_NOW = datetime.now(pytz.UTC)
                    if UTC_TIME_NOW > otp_expiry_time:
                        return common_response_format(
                            False,
                            [],
                            "OTP expired.",
                            RESPONSE_CODE_400,
                            HTTP_RESPONSE_STATUS_400,
                        )
                    User.objects.filter(email=email_id).update(
                        password=make_password(password)
                    )
                    return common_response_format(
                        True,
                        [],
                        "Password updated successfully.",
                        RESPONSE_CODE_200,
                        HTTP_RESPONSE_STATUS_200,
                    )
                else:
                    return common_response_format(
                        False,
                        [],
                        "Invalid OTP.",
                        RESPONSE_CODE_400,
                        HTTP_RESPONSE_STATUS_400,
                    )
            else:
                return common_response_format(
                    False,
                    [],
                    serializer.errors,
                    RESPONSE_CODE_400,
                    HTTP_RESPONSE_STATUS_400,
                )
        except Exception as e:
            return common_response_format(
                False,
                [],
                "Internal server error. Please try again later...",
                RESPONSE_CODE_500,
                HTTP_RESPONSE_STATUS_500,
            )
