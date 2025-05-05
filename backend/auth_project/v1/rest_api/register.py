from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from v1.models import EmailVerification
from v1.serializers.register import LoginSerializers
from v1.utils.response_util import common_response_format
from v1.constants.constants import (
    RESPONSE_CODE_201,
    RESPONSE_CODE_400,
    RESPONSE_CODE_500,
    HTTP_RESPONSE_STATUS_201,
    HTTP_RESPONSE_STATUS_400,
    HTTP_RESPONSE_STATUS_500,
)


class UserRegister(APIView):
    """This endpoint is used to register a new user in the Django auth user table."""

    def post(self, request):
        try:
            serializer = LoginSerializers(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                username = data["username"]
                password = data["password"]
                email = data["email"]
                first_name = data["first_name"] if "first_name" in data else None
                last_name = data["last_name"] if "last_name" in data else None
                is_staff = data["is_staff"] if "is_staff" in data else False
                is_active = data["is_active"] if "is_active" in data else False
                is_superuser = data["is_superuser"] if "is_superuser" in data else False
                # Verify whether the email address is verified or not.
                try:
                    email_status = EmailVerification.objects.get(email=email)
                    if not email_status.verified:
                        return common_response_format(
                            False,
                            [],
                            "Email ID is not verified.",
                            RESPONSE_CODE_400,
                            HTTP_RESPONSE_STATUS_400,
                        )
                except:
                    return common_response_format(
                        False,
                        [],
                        "Email ID is not verified.",
                        RESPONSE_CODE_400,
                        HTTP_RESPONSE_STATUS_400,
                    )

                User.objects.create(
                    username=username,
                    password=make_password(password),
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=is_staff,
                    is_active=is_active,
                    is_superuser=is_superuser,
                )
                return common_response_format(
                    True,
                    [],
                    "User created successfully.",
                    RESPONSE_CODE_201,
                    HTTP_RESPONSE_STATUS_201,
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
