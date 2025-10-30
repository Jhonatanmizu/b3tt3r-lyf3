from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views.user_detail_view import UserRetrieveUpdateDestroy
from authentication.views.user_list_view import UserListCreate

app_name = "auth"


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListCreate.as_view(), name="user-list"),
    path("users/<str:pk>", UserRetrieveUpdateDestroy.as_view(), name="user-detail"),
]
