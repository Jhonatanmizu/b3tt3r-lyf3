from __future__ import annotations

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from core.models.base import BaseModel


class CustomUserManager(UserManager):
    def get_queryset(self) -> models.QuerySet[CustomUser]:
        return super().get_queryset().filter(is_deleted=False)


class Profile(BaseModel):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    profile_picture = models.ImageField(default=None, blank=True, null=True)
    biography = models.TextField(max_length=200, default="", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.pk)


class CustomUser(AbstractUser, BaseModel):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = "User"
        verbose_name_plural = "Users"

    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True
    )
    timezone = models.CharField(max_length=64, default="UTC")
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    objects: CustomUserManager = CustomUserManager()  # pyright: ignore[reportIncompatibleVariableOverride]
    all_objects: models.Manager[CustomUser] = models.Manager()  # pyright: ignore[reportIncompatibleVariableOverride]

    def add_xp(self, amount: int) -> None:
        self.xp += amount
        while self.xp >= self.level * 100:
            self.level += 1
        self.save(update_fields=["xp", "level"])

    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self) -> str:
        return f"{self.pk}-{self.first_name}-{self.last_name}"
