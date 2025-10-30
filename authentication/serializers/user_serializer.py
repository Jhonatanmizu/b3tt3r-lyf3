from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "level",
            "xp",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")
