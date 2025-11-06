from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "level",
            "xp",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
