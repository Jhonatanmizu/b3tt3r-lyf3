from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.serializers.user_serializer import CustomUserSerializer
from core.views.authenticated_views import AuthenticatedGenericAPIView


@extend_schema(
    tags=["Users"],
    summary="Current User",
    description="Retrieve the profile data of the currently authenticated user.",
    responses={200: CustomUserSerializer},
)
class UserDataView(AuthenticatedGenericAPIView):
    serializer_class = CustomUserSerializer

    def get(self, request: Request, *_args, **_kwargs) -> Response:
        """
        Retrieve and return the authenticated user's data.

        Note:
            This endpoint requires authentication.
        """
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=200)
