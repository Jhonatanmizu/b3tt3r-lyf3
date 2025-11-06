from rest_framework.permissions import IsAuthenticated

from authentication.serializers.user_serializer import CustomUserSerializer
from core.views.authenticated_views import AuthenticatedListCreateAPIView
from users.models import CustomUser


class UserListCreate(AuthenticatedListCreateAPIView):
    """
    View to list all users or create a new user.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    queryset = CustomUser.soft_deleted_objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
