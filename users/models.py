from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models.base import BaseModel


class Profile(BaseModel):
    profile_picture = models.ImageField(default=None, blank=True, null=True)
    biography = models.TextField(max_length=200, default="", blank=True, null=True)


class CustomUser(BaseModel, AbstractUser):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True
    )
