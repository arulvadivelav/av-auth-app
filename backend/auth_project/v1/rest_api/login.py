import jwt

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from datetime import datetime, timedelta

from v1.serializers.login_serializer import PasswordSerializer
from v1.utils.response_util import common_response_format
from v1.constants.constants import (
    RESPONSE_CODE_200,
    RESPONSE_CODE_400,
    RESPONSE_CODE_500,
    HTTP_RESPONSE_STATUS_200,
    HTTP_RESPONSE_STATUS_400,
    HTTP_RESPONSE_STATUS_500,
)


class Login(APIView):
    """This endpoint is used to authenticate the logged user."""

    def post(self, request):
        try:
            serializer = PasswordSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                # Check user details exist or not based on the email.
                check_user = User.objects.filter(
                    email=validated_data["email_id"]
                ).first()
                if check_user:
                    # Password verification
                    check_pw = check_password(
                        validated_data["password"], check_user.password
                    )
                    if check_pw:
                        # Token generation with the payload details
                        payload = {
                            "user_id": check_user.id,
                            "exp": datetime.now() + timedelta(hours=1),
                        }
                        token = jwt.encode(
                            payload, settings.SECRET_KEY, algorithm="HS256"
                        )
                        final_result = {"token": token}
                        return common_response_format(
                            True,
                            final_result,
                            "Logged in successfully.",
                            RESPONSE_CODE_200,
                            HTTP_RESPONSE_STATUS_200,
                        )
                    else:
                        return common_response_format(
                            False,
                            [],
                            "Wrong password.",
                            RESPONSE_CODE_400,
                            HTTP_RESPONSE_STATUS_400,
                        )
                else:
                    return common_response_format(
                        False,
                        [],
                        "Invalid username.",
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
