from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from authentication.serializers.user_serializer import CustomUserSerializer
from core.views.authenticated_views import AuthenticatedListCreateAPIView
from users.models import CustomUser


@extend_schema(
    tags=["Users"],
    summary="List / Create Users",
    description=(
        "List all users or create a new user. Requires authentication."
    ),
    responses={
        200: CustomUserSerializer(many=True),
        201: CustomUserSerializer,
    },
)
class UserListCreate(AuthenticatedListCreateAPIView):
    """
    View to list all users or create a new user.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    queryset = CustomUser.all_objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
