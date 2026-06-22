"""Password reset request view — sends a reset link via Resend."""

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers.auth_serializers import PasswordResetRequestSerializer
from core.email import send_email
from django.conf import settings

User = get_user_model()


@extend_schema(
    tags=["Authentication"],
    summary="Request Password Reset",
    description=(
        "Send a password reset email to the provided address if a matching user exists. "
        "Always returns 200 to prevent email enumeration."
    ),
    request=PasswordResetRequestSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"},
            },
        },
    },
)
class PasswordResetRequestView(APIView):
    permission_classes: ClassVar[list[AllowAny]] = [AllowAny]

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.all_objects.filter(email__iexact=email).first()
        if user is not None and user.is_active:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = (
                f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?uid={uid}&token={token}"
            )

            template_id = settings.RESEND_PASSWORD_RESET_TEMPLATE_ID
            if template_id:
                send_email(
                    to=user.email,
                    template_id=template_id,
                    data={
                        "username": user.get_username(),
                        "reset_url": reset_url,
                    },
                )
            else:
                send_email(
                    to=user.email,
                    subject="Password Reset Request",
                    text=(
                        f"Hi {user.get_username()},\n\n"
                        f"You requested a password reset. Click the link below:\n"
                        f"{reset_url}\n\n"
                        f"If you didn't request this, you can ignore this email."
                    ),
                    html=(
                        f"<p>Hi {user.get_username()},</p>"
                        f"<p>You requested a password reset. Click the link below:</p>"
                        f'<p><a href="{reset_url}">Reset Password</a></p>'
                        f"<p>If you didn't request this, you can ignore this email.</p>"
                    ),
                )

        return Response(
            {"detail": "If an account with that email exists, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )
