from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.serializers.user_serializer import CustomUserSerializer


class UserDataView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Return the user's data."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
