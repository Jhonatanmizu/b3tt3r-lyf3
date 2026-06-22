"""Tests for the complete authentication flow."""

from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


class AuthFlowTests(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpassword123",
            first_name="Test",
            last_name="User",
        )
        self.user.is_active = True
        self.user.save()

    # ─── Login ─────────────────────────────────────────────────────────

    def test_login_success(self) -> None:
        url = reverse("auth:login")
        response = self.client.post(
            url, {"username": "testuser", "password": "strongpassword123"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_failure(self) -> None:
        url = reverse("auth:login")
        response = self.client.post(
            url, {"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ─── Register ──────────────────────────────────────────────────────

    def test_register_success(self) -> None:
        url = reverse("auth:register")
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newstrongpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.all_objects.filter(username="newuser").exists()

    def test_register_duplicate_email(self) -> None:
        url = reverse("auth:register")
        payload = {
            "username": "another",
            "email": "test@example.com",
            "password": "newstrongpassword123",
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # ─── Token Refresh ─────────────────────────────────────────────────

    def test_token_refresh_success(self) -> None:
        refresh = RefreshToken.for_user(self.user)
        url = reverse("auth:token_refresh")
        response = self.client.post(url, {"refresh": str(refresh)})
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_refresh_invalid(self) -> None:
        url = reverse("auth:token_refresh")
        response = self.client.post(url, {"refresh": "invalid-token"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ─── Logout ────────────────────────────────────────────────────────

    def test_logout_blacklists_token(self) -> None:
        refresh = RefreshToken.for_user(self.user)
        url = reverse("auth:logout")
        response = self.client.post(url, {"refresh": str(refresh)})
        assert response.status_code == status.HTTP_205_RESET_CONTENT

    def test_logout_invalid_token(self) -> None:
        url = reverse("auth:logout")
        response = self.client.post(url, {"refresh": "invalid-token"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # ─── Password Reset Request ────────────────────────────────────────

    @patch("authentication.views.password_reset_request_view.send_email")
    def test_password_reset_request_sends_email(self, mock_send_email) -> None:
        mock_send_email.return_value = {"id": "email-id"}
        url = reverse("auth:password_reset")
        response = self.client.post(url, {"email": "test@example.com"})
        assert response.status_code == status.HTTP_200_OK
        mock_send_email.assert_called_once()

    @patch("authentication.views.password_reset_request_view.send_email")
    def test_password_reset_request_nonexistent_email(self, mock_send_email) -> None:
        url = reverse("auth:password_reset")
        response = self.client.post(url, {"email": "nobody@example.com"})
        assert response.status_code == status.HTTP_200_OK
        mock_send_email.assert_not_called()

    # ─── Password Reset Confirm ────────────────────────────────────────

    def test_password_reset_confirm_success(self) -> None:
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        url = reverse("auth:password_reset_confirm")
        payload = {
            "uid": uid,
            "token": token,
            "new_password": "brandnewpassword123",
            "confirm_password": "brandnewpassword123",
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK

        self.user.refresh_from_db()
        assert self.user.check_password("brandnewpassword123")

    def test_password_reset_confirm_invalid_token(self) -> None:
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = reverse("auth:password_reset_confirm")
        payload = {
            "uid": uid,
            "token": "invalid-token",
            "new_password": "brandnewpassword123",
            "confirm_password": "brandnewpassword123",
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_reset_confirm_password_mismatch(self) -> None:
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        url = reverse("auth:password_reset_confirm")
        payload = {
            "uid": uid,
            "token": token,
            "new_password": "brandnewpassword123",
            "confirm_password": "differentpassword123",
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # ─── User Data ─────────────────────────────────────────────────────

    def test_user_data_authenticated(self) -> None:
        self.client.force_authenticate(user=self.user)
        url = reverse("auth:user-data")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "testuser"

    def test_user_data_unauthenticated(self) -> None:
        url = reverse("auth:user-data")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
