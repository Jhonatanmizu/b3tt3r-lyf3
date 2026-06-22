from drf_spectacular.utils import extend_schema

from authentication.serializers.user_serializer import CustomUserSerializer
from core.views.authenticated_views import AuthenticatedRetrieveUpdateDestroyAPIView
from users.models import CustomUser


@extend_schema(
    tags=["Users"],
    summary="Retrieve / Update / Delete User",
    description=(
        "Retrieve, update, or delete a specific user by primary key. "
        "Requires authentication."
    ),
    responses={
        200: CustomUserSerializer,
        204: {"description": "User deleted successfully."},
    },
)
class UserRetrieveUpdateDestroy(AuthenticatedRetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific user by primary key.

    * Requires token authentication.
    * Only admin users are able to access this view
    (or the user themselves for update/retrieve).
    """

    queryset = CustomUser.all_objects.all()
    serializer_class = CustomUserSerializer
