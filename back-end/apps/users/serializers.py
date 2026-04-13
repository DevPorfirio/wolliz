import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


# ─── Input Serializers ────────────────────────────────────────────────────────

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=8, write_only=True)
    phone = serializers.CharField(max_length=20, default="", allow_blank=True)

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome não pode ser vazio.")
        return value.strip()

    def validate_phone(self, value):
        if value and not re.match(r"^\+?[\d\s\-\(\)]{8,22}$", value):
            raise serializers.ValidationError(
                "Formato de telefone inválido. Ex: +55 DD 99999-9999"
            )
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class ProfileUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False, allow_null=True)
    phone = serializers.CharField(
        max_length=20, required=False, allow_null=True, allow_blank=True
    )

    def validate_name(self, value):
        if value is not None and not value.strip():
            raise serializers.ValidationError("O nome não pode ser vazio.")
        return value.strip() if value else value

    def validate_phone(self, value):
        if value and not re.match(r"^\+?[\d\s\-\(\)]{8,22}$", value):
            raise serializers.ValidationError(
                "Formato de telefone inválido. Ex: +55 DD 99999-9999"
            )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


# ─── Output Serializers ───────────────────────────────────────────────────────

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()
    phone = serializers.CharField()
    avatar_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_avatar_url(self, obj):
        if obj.avatar:
            try:
                return obj.avatar.url
            except Exception:
                pass
        return None
