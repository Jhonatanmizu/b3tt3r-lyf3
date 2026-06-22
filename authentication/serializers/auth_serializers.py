"""Authentication-specific DRF serializers."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for obtaining JWT access/refresh token pair."""

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        fields = ("username", "password")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(write_only=True)
        self.fields["password"] = serializers.CharField(
            write_only=True, style={"input_type": "password"}
        )


class TokenRefreshAPIViewSerializer(TokenRefreshSerializer):
    """Serializer for refreshing an access token using a refresh token."""

    refresh = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    """Serializer for logging out (blacklisting a refresh token)."""

    refresh = serializers.CharField(
        write_only=True,
        help_text="The refresh token to blacklist.",
    )


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting a password reset email."""

    email = serializers.EmailField(
        required=True,
        help_text="The email address associated with the user account.",
    )


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a password reset."""

    uid = serializers.CharField(
        required=True,
        help_text="Base64-encoded user ID from the reset link.",
    )
    token = serializers.CharField(
        required=True,
        help_text="Reset token from the reset link.",
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="The new password.",
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Repeat the new password for confirmation.",
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": _("The two password fields didn't match.")},
            )
        validate_password(attrs["new_password"])
        return attrs
