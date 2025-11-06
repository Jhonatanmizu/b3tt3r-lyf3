from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class AuthenticatedAPIView(generics.GenericAPIView):
    """
    A base view that requires authentication for access.
    """

    permission_classes = [IsAuthenticated]


class AuthenticatedRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    A base view that requires authentication for access.
    """

    permission_classes = [IsAuthenticated]


class AuthenticatedListCreateAPIView(generics.ListCreateAPIView):
    """
    A base list create view that requires authentication for access.
    """

    permission_classes = [IsAuthenticated]
