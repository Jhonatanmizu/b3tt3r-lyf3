"""Password reset confirmation view — validates token and sets new password."""

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers.auth_serializers import PasswordResetConfirmSerializer

User = get_user_model()


@extend_schema(
    tags=["Authentication"],
    summary="Confirm Password Reset",
    description=(
        "Confirm a password reset using the uid and token received via email, "
        "and set a new password."
    ),
    request=PasswordResetConfirmSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"},
            },
        },
        400: {"description": "Invalid token, uid, or password mismatch"},
    },
)
class PasswordResetConfirmView(APIView):
    permission_classes: ClassVar[list[AllowAny]] = [AllowAny]

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.all_objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired reset token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
