from django.urls import path

from authentication.views.login_view import LoginView
from authentication.views.logout_view import LogoutView
from authentication.views.password_reset_confirm_view import PasswordResetConfirmView
from authentication.views.password_reset_request_view import PasswordResetRequestView
from authentication.views.register_view import RegisterView
from authentication.views.token_refresh_view import TokenRefreshAPIView
from authentication.views.user_data_view import UserDataView
from authentication.views.user_detail_view import UserRetrieveUpdateDestroy
from authentication.views.user_list_view import UserListCreate

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("users/", UserListCreate.as_view(), name="user-list"),
    path("users/me/", UserDataView.as_view(), name="user-data"),
    path("users/<str:pk>/", UserRetrieveUpdateDestroy.as_view(), name="user-detail"),
]