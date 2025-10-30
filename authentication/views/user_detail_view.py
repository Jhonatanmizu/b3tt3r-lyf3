from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers.user_serializer import CustomUserSerializer
from users.models import CustomUser


class UserRetrieveUpdateDestroy(APIView):
    """
    View to retrieve, update, or delete a specific user by primary key.

    * Requires token authentication.
    * Only admin users are able to access this view
    (or the user themselves for update/retrieve).
    """

    def get_object(self, pk: int):
        """Helper method to get the user object or raise a 404."""
        try:
            return CustomUser.soft_deleted_objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        Retrieve a specific user.
        """
        user = self.get_object(pk)
        if user is None:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        Update an entire user record (PUT).
        """
        user = self.get_object(pk)
        if user is None:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        """
        Delete a user (or soft-delete them if using soft-deletion).
        """
        user = CustomUser.soft_deleted_objects.filter(pk=pk).first()
        if user is None:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
