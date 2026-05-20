from typing import ClassVar

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.serializers.user_serializer import CustomUserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes: ClassVar[list[AllowAny]] = [AllowAny]

    def create(self, request: Request, *_args: object, **_kwargs: object) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            CustomUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )
