from __future__ import annotations

from typing import Optional
import uuid
from django.db import models
from django.utils import timezone

# ---------- Manager ----------
class SoftDeleteManager(models.Manager["BaseModel"]):
    """Default manager that hides logically deleted records."""

    def get_queryset(self) -> models.QuerySet["BaseModel"]:
        return super().get_queryset().filter(is_deleted=False)


# ---------- Abstract Base Model ----------
class BaseModel(models.Model):
    """
    Abstract base model with:
      - created_at / updated_at timestamps
      - is_active flag
      - soft delete (is_deleted, deleted_at)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Managers
    objects = SoftDeleteManager()
    all_objects: models.Manager["BaseModel"] = models.Manager()

    # ----- Soft Delete -----
    def delete(self, using: Optional[str] = None, keep_parents: bool = False) -> tuple:
        """Soft delete the record (mark as deleted instead of removing)."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
        return (
            self.pk,
            {
                "id": self.pk,
                "is_deleted": self.is_deleted,
                "deleted_at": self.deleted_at,
            },
        )

    def restore(self) -> None:
        """Restore a previously soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

    class Meta:
        abstract = True 

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.pk})"