from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.serializers.user_serializer import CustomUserSerializer
from users.models import CustomUser


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific user by primary key.

    * Requires token authentication.
    * Only admin users are able to access this view
    (or the user themselves for update/retrieve).
    """

    queryset = CustomUser.soft_deleted_objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
