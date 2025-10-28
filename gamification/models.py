from django.db import models

from core.models.base import BaseModel
from users.models import CustomUser


class Reward(BaseModel):
    """
    Defines purchasable rewards (items, privileges, skins, etc.) for the shop.
    """

    class Meta(BaseModel.Meta):
        verbose_name = "Reward"
        verbose_name_plural = "Rewards"

    TYPE_CHOICES = [
        ("item", "In-Game Item"),
        ("privilege", "Real-Life Privilege"),
        ("cosmetic", "Cosmetic/Skin"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    cost_xp = models.PositiveIntegerField(
        default=100, help_text="The amount of XP required to purchase this reward."
    )
    reward_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="item")

    def __str__(self):
        return f"Reward: {self.name} (Cost: {self.cost_xp} XP)"


class UserReward(BaseModel):
    """
    Tracks which rewards a user has purchased (their inventory).
    Inherits BaseModel to track soft-delete and timestamps.
    """

    class Meta(BaseModel.Meta):
        verbose_name = "User Reward"
        verbose_name_plural = "User Rewards"

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="purchased_rewards"
    )
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)

    is_used = models.BooleanField(default=False)

    def use(self):
        """Marks a consumable reward as used."""
        if not self.is_used:
            self.is_used = True
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"

    def purchased_at(self):
        """Returns the timestamp when the reward was purchased."""
        return self.created_at


class Badge(BaseModel):
    """
    Defines achievements/milestones users can unlock.
    Updated to inherit BaseModel for UUID primary key and soft-delete.
    """

    class Meta(BaseModel.Meta):
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.URLField(blank=True, null=True)
    xp_required = models.PositiveIntegerField(
        help_text="The minimum total XP required to be eligible for this badge."
    )

    def __str__(self):
        return self.name


class UserBadge(BaseModel):
    """
    Tracks which badges a user has been awarded.
    Updated to inherit BaseModel for UUID primary key and soft-delete.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="awarded_badges"
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"
        unique_together = ("user", "badge")

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

    def awarded_at(self):
        """Returns the timestamp when the badge was awarded."""
        return self.created_at
