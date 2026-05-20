from __future__ import annotations

from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest

from users.models import CustomUser, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "biography")
    search_fields = ("biography",)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "level",
        "xp",
        "timezone",
        "is_deleted",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_deleted", "is_active", "is_staff", "timezone", "level")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets: tuple[tuple[str | None, dict[str, Any]], ...] = (  # pyright: ignore[reportIncompatibleVariableOverride]
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Game Info", {"fields": ("xp", "level")}),
        ("Preferences", {"fields": ("timezone",)}),
        ("Profile", {"fields": ("profile",)}),
        (
            "Soft Delete",
            {
                "fields": ("is_deleted", "deleted_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("deleted_at",)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return CustomUser.all_objects.all()

    def delete_model(self, request: HttpRequest, obj: CustomUser) -> None:
        obj.delete()

    def delete_queryset(
        self, request: HttpRequest, queryset: QuerySet[CustomUser]
    ) -> None:
        for obj in queryset:
            obj.delete()
