import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from productivity.models import Goal, Habit, HabitEntry, JournalEntry, Task

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Seeds the database with initial development data for Better Lyfe Project"
        " using bulk_create."
    )

    def handle(self, *args, **options):
        self.stdout.write("--- Starting Database Seeding ---")

        Task.objects.all().delete()
        JournalEntry.objects.all().delete()
        HabitEntry.objects.all().delete()
        Habit.objects.all().delete()
        Goal.objects.all().delete()
        User.objects.filter(
            email__in=["alice@betterlyfe.dev", "bob@betterlyfe.dev"]
        ).delete()

        self.stdout.write("Creating Users...")
        alice = User.objects.create(
            username="alice_j",
            email="alice@betterlyfe.dev",
            password="testpassword123",
            first_name="Alice",
            last_name="Johnson",
        )
        bob = User.objects.create(
            username="bob_s",
            email="bob@betterlyfe.dev",
            password="testpassword123",
            first_name="Bob",
            last_name="Smith",
        )

        self.stdout.write("Creating Goals...")

        goals = [
            Goal(
                user=alice,
                name="Finish Personal Project",
                description='Complete and launch the "ZenGarden" mobile app.',
                target_date=date(2025, 12, 31),
                status="In Progress",
            ),
            Goal(
                user=alice,
                name="Run a 10K Marathon",
                description="Complete a 10-kilometer race.",
                target_date=date(2026, 6, 1),
                status="Planning",
            ),
            Goal(
                user=bob,
                name="Read 12 Books",
                description="Finish one book per month for the year.",
                target_date=date(2025, 12, 31),
                status="In Progress",
            ),
        ]
        Goal.objects.bulk_create(goals)

        goal_a1 = Goal.objects.get(user=alice, name="Finish Personal Project")
        goal_b1 = Goal.objects.get(user=bob, name="Read 12 Books")

        self.stdout.write("Creating Habits...")

        habits = [
            Habit(
                user=alice,
                name="Daily Code Review",
                frequency="Daily",
            ),
            Habit(
                user=alice,
                name="Meditate",
                frequency="Daily",
            ),
            Habit(
                user=bob,
                name="Read for 20 Mins",
                frequency="Daily",
            ),
        ]
        Habit.objects.bulk_create(habits)

        habit_a1 = Habit.objects.get(user=alice, name="Daily Code Review")
        habit_a2 = Habit.objects.get(user=alice, name="Meditate")
        habit_b1 = Habit.objects.get(user=bob, name="Read for 20 Mins")

        self.stdout.write("Logging Habit Entries...")
        entries_to_create = []
        today = date.today()
        num_days = 9

        for i in range(1, num_days + 1):
            log_date = today - timedelta(days=i)

            is_completed_a1 = random.choice([True] * 9 + [False] * 1)
            entries_to_create.append(
                HabitEntry(habit=habit_a1, date=log_date, completed=is_completed_a1)
            )

            entries_to_create.append(
                HabitEntry(habit=habit_a2, date=log_date, completed=True)
            )

            is_completed_b1 = random.choice([True] * 6 + [False] * 3)
            entries_to_create.append(
                HabitEntry(habit=habit_b1, date=log_date, completed=is_completed_b1)
            )

        HabitEntry.objects.bulk_create(entries_to_create)

        self.stdout.write("Creating Tasks...")
        tasks_to_create = [
            Task(
                user=alice,
                goal=goal_a1,
                description="Design ZenGarden wireframes",
                due_date=date(2025, 11, 15),
                title="Design Wireframes",
            ),
            Task(
                user=alice,
                goal=goal_a1,
                description="Setup CI/CD pipeline",
                due_date=date(2025, 10, 20),
                title="Setup CI/CD Pipeline",
            ),
            Task(
                user=alice,
                goal=None,
                description="Buy new desk chair",
                due_date=date(2025, 11, 1),
                title="Purchase Desk Chair",
            ),
            Task(
                user=bob,
                goal=goal_b1,
                description='Check out "The Martian" from library',
                due_date=date(2025, 11, 1),
                title="Check Out The Martian",
            ),
        ]

        Task.objects.bulk_create(tasks_to_create)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database! 🌱"))
