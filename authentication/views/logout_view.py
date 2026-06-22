"""Logout view that blacklists the provided refresh token."""

from typing import ClassVar

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers.auth_serializers import LogoutSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Logout",
    description=(
        "Blacklist the provided refresh token so it can no longer be used "
        "to obtain new access tokens."
    ),
    request=LogoutSerializer,
    responses={
        205: {"description": "Token successfully blacklisted"},
        400: {"description": "Bad request (invalid or missing token)"},
    },
)
class LogoutView(APIView):
    permission_classes: ClassVar[list[AllowAny]] = [AllowAny]

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT,
        )
