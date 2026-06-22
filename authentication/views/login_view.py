"""Login view returning JWT access and refresh tokens."""

from typing import ClassVar

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers.auth_serializers import LoginSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Login",
    description="Authenticate with username and password to receive a JWT access/refresh token pair.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
                "refresh": {"type": "string"},
            },
        },
        401: {"description": "Invalid credentials"},
    },
)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes: ClassVar[list[AllowAny]] = [AllowAny]

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        return super().post(request, *args, **kwargs)
