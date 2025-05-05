from rest_framework import serializers


class PasswordSerializer(serializers.Serializer):
    email_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
