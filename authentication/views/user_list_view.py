from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers.user_serializer import CustomUserSerializer
from users.models import CustomUser


class UserListCreate(APIView):
    """
    View to list all users or create a new user.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request: Request, format=None) -> Response:
        """
        Return a list of all active users.
        """
        users = CustomUser.soft_deleted_objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None) -> Response:
        """
        Create a new user.
        """
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
