from rest_framework.response import Response


def common_response_format(status_flag, data, message, status_code, http_status):
    return Response(
        {
            "status": status_flag,
            "data": data,
            "message": message,
            "status_code": status_code,
        },
        status=http_status,
    )
