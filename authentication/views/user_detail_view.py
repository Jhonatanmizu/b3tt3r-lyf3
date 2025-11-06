from authentication.serializers.user_serializer import CustomUserSerializer
from core.views.authenticated_views import AuthenticatedRetrieveUpdateDestroyAPIView
from users.models import CustomUser


class UserRetrieveUpdateDestroy(AuthenticatedRetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific user by primary key.

    * Requires token authentication.
    * Only admin users are able to access this view
    (or the user themselves for update/retrieve).
    """

    queryset = CustomUser.soft_deleted_objects.all()
    serializer_class = CustomUserSerializer
