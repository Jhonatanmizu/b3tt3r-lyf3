from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models.base import BaseModel, SoftDeleteManager


class Profile(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"

    profile_picture = models.ImageField(default=None, blank=True, null=True)
    biography = models.TextField(max_length=200, default="", blank=True, null=True)

    def __str__(self) -> str:
        return self.pk


class CustomUser(AbstractUser, BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"

    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True
    )
    timezone = models.CharField(max_length=64, default="UTC")
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    objects: models.Manager["CustomUser"] = models.Manager()  # type: ignore
    soft_deleted_objects: models.Manager["CustomUser"] = SoftDeleteManager()  # type: ignore

    def add_xp(self, amount):
        """Add XP and handle level-up logic."""
        self.xp += amount
        while self.xp >= self.level * 100:
            self.level += 1
        self.save()

    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.pk}-{self.first_name}-{self.last_name}"
