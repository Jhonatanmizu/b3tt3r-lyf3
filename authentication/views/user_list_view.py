from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.serializers.user_serializer import CustomUserSerializer
from users.models import CustomUser


class UserListCreate(generics.ListCreateAPIView):
    """
    View to list all users or create a new user.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    queryset = CustomUser.soft_deleted_objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
