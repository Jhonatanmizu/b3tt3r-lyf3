from django.contrib.auth.password_validation import validate_password
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

    def validate_email(self, value: str) -> str:
        if CustomUser.all_objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> CustomUser:
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
