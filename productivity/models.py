from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.models.base import BaseModel

User = settings.AUTH_USER_MODEL


class Tag(BaseModel):
    """
    Tags used to categorize Tasks, Goals, or Journal Entries.
    """

    class Meta(BaseModel.Meta):
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default="#3b82f6")

    def __str__(self):
        return self.name


class Goal(BaseModel):
    """
    Long-term objective that can group related Tasks and Habits.
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    target_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    current_value = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0)
    )
    target_date = models.DateField(null=True, blank=True)
    completion_xp_reward = models.PositiveIntegerField(default=50)

    def mark_completed(self):
        """Sets the goal to completed and awards a large XP bonus."""
        if self.status != "completed":
            self.status = "completed"
            self.save()
            self.user.add_xp(self.completion_xp_reward)

    def __str__(self):
        return f"Goal: {self.name} ({self.status})"

    class Meta(BaseModel.Meta):
        verbose_name = "Goal"
        verbose_name_plural = "Goals"
        ordering = ["target_date"]


class Task(BaseModel):
    """
    Short-term, actionable items for the user.
    """

    class Meta(BaseModel.Meta):
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("archived", "Archived"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    tags = models.ManyToManyField(Tag, blank=True)

    goal = models.ForeignKey(
        Goal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_tasks",
    )

    def mark_done(self):
        """Marks task as done and awards XP."""
        if self.status != "done":
            self.status = "done"
            self.save()
            self.user.add_xp(10)

    def __str__(self):
        return f"{self.title} ({self.status})"


class Habit(BaseModel):
    """
    Recurring, long-term actions to track consistency (streaks).
    """

    class Meta(BaseModel.Meta):
        verbose_name = "Habit"
        verbose_name_plural = "Habits"

    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=255)
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default="daily"
    )
    streak = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)

    goal = models.ForeignKey(
        Goal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",
    )

    def complete(self, date=None):
        """Mark habit as complete for a given day and update streak."""
        if date is None:
            date = timezone.localdate()

        if self.last_completed:
            delta = date - self.last_completed
            # Simple streak logic: only continue if completed yesterday
            if delta.days == 1:
                self.streak += 1
            elif delta.days > 1:
                self.streak = 1
        else:
            self.streak = 1

        self.last_completed = date
        self.save()
        self.user.add_xp(5)

    def __str__(self):
        return f"{self.name} (Streak: {self.streak})"


class JournalEntry(BaseModel):
    """
    For daily logging, reflections, and mood tracking.
    """

    MOOD_CHOICES = [
        (1, "Terrible"),
        (2, "Bad"),
        (3, "Neutral"),
        (4, "Good"),
        (5, "Amazing"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="journal_entries"
    )

    entry_date = models.DateField(default=timezone.localdate, db_index=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    mood_rating = models.PositiveSmallIntegerField(
        choices=MOOD_CHOICES,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"Journal on {self.entry_date} by {self.user.username}"

    class Meta(BaseModel.Meta):
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"
        unique_together = ("user", "entry_date")
        ordering = ["-entry_date"]
        ordering = ["-entry_date"]
        ordering = ["-entry_date"]
        ordering = ["-entry_date"]


class HabitEntry(BaseModel):
    """
    Represents a single log or attempt to complete a specific Habit on a given date.
    This model is crucial for tracking streaks, compliance, and history.
    """

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="entries",
        help_text="The habit this entry is logging.",
    )

    # 2. Date of the entry
    date = models.DateField(help_text="The date this habit was tracked for.")

    # 3. Status/Completion
    completed = models.BooleanField(
        default=False,
        help_text=(
            "Whether the habit was completed (True) or "
            "missed/skipped (False) on this date."
        ),
    )

    # 4. (Optional) Quantity/Value
    # For a quantitative habit (e.g., "Drink 8 glasses of water"):
    # value = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     help_text="The numeric value recorded for the habit (e.g., steps, glasses of water, pages read)."
    # )

    class Meta(BaseModel.Meta):
        unique_together = ("habit", "date")
        ordering = ["date"]
        verbose_name = "Habit Log Entry"
        verbose_name_plural = "Habit Log Entries"

    def __str__(self):
        status = "Completed" if self.completed else "Missed"
        return f"[{self.date}] {self.habit.name}: {status}"
