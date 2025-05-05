from rest_framework import serializers
from django.contrib.auth.models import User
import re


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, max_length=20)
    confirm_password = serializers.CharField(required=True, max_length=20)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=20)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=20)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exist.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password required.")
        if len(value) <= 8:
            raise serializers.ValidationError("Pasword length should be at least 8.")

        has_digit = any(char.isdigit() for char in value)
        has_upper = any(char.isupper() for char in value)
        has_lower = any(char.islower() for char in value)
        has_spec = any(char in "#@!%*<>^" for char in value)

        if not has_digit:
            raise serializers.ValidationError(
                "Password should have at least one numeral"
            )
        if not has_upper:
            raise serializers.ValidationError(
                "Password should have at least one uppercase letter"
            )
        if not has_lower:
            raise serializers.ValidationError(
                "Password should have at least one lowercase letter"
            )
        if not has_spec:
            raise serializers.ValidationError(
                "Password should have at least one of the symbols #@!%*<>^"
            )
        return value

    def validate_email(self, value):
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(value, email_pattern):
            raise serializers.ValidationError("Invalid email address")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already exist.")
        return value

    def validate_confirm_password(self, value):
        if not value:
            raise serializers.ValidationError("Confirm password is required.")
        if value != self.initial_data["password"]:
            raise serializers.ValidationError(
                "New password and confirm password should not match."
            )
        return value


class OtpSerializer(serializers.Serializer):
    email_id = serializers.EmailField(required=True)

    def validate_email_id(self, value):
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(value, email_pattern):
            raise serializers.ValidationError("Invalid email address.")
        return value


class ForgotSerializer(serializers.Serializer):
    email_id = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_email_id(self, value):
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(value, email_pattern):
            raise serializers.ValidationError("Invalid email address")
        return value

    def validate_new_password(self, value):
        if not value:
            raise serializers.ValidationError("Password required.")
        if len(value) < 8:
            raise serializers.ValidationError("Pasword length should be at least 8.")

        has_digit = any(char.isdigit() for char in value)
        has_upper = any(char.isupper() for char in value)
        has_lower = any(char.islower() for char in value)
        has_spec = any(char in "#@!%*<>^" for char in value)

        if not has_digit:
            raise serializers.ValidationError(
                "Password should have at least one numeral"
            )
        if not has_upper:
            raise serializers.ValidationError(
                "Password should have at least one uppercase letter"
            )
        if not has_lower:
            raise serializers.ValidationError(
                "Password should have at least one lowercase letter"
            )
        if not has_spec:
            raise serializers.ValidationError(
                "Password should have at least one of the symbols #@!%*<>^"
            )
        return value

    def validate_confirm_password(self, value):
        if not value:
            raise serializers.ValidationError("Confirm password is required.")
        if value != self.initial_data["new_password"]:
            raise serializers.ValidationError(
                "New password and confirm password should not match."
            )
        return value
