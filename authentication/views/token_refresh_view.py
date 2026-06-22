"""Token refresh view returning a new access token."""

from typing import ClassVar

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.serializers.auth_serializers import TokenRefreshAPIViewSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Refresh Token",
    description="Exchange a valid refresh token for a new access token.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
            },
        },
        401: {"description": "Invalid or expired refresh token"},
    },
)
class TokenRefreshAPIView(TokenRefreshView):
    serializer_class = TokenRefreshAPIViewSerializer
    permission_classes: ClassVar[list[AllowAny]] = [AllowAny]

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        return super().post(request, *args, **kwargs)
