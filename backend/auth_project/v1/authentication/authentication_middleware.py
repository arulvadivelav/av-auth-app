from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from auth_project.settings import SECRET_KEY, EXCEPTION_URLS
from django.contrib.auth.models import User
import jwt


class CustomAuthentication(APIView):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in EXCEPTION_URLS:
            return self.get_response(request)

        auth_header = request.headers.get("Authorization")
        try:
            if auth_header:
                token = auth_header
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    user_reff = User.objects.filter(id=payload["user_id"]).last()
                    if not user_reff:
                        return JsonResponse(
                            {
                                "status": False,
                                "message": "User not found.",
                                "status_code": 400,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                except Exception as e:
                    print(e)
                    return JsonResponse(
                        {
                            "status": False,
                            "message": "Something went wrong.",
                            "status_code": 500,
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return JsonResponse(
                    {"status": False, "message": "Token required.", "status_code": 400},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {"status": False, "message": "Token expired.", "status_code": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return self.get_response(request)
