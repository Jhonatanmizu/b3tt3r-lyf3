"""Management command to remove expired blacklisted tokens.

This command wraps ``flushexpiredtokens`` from
``rest_framework_simplejwt.token_blacklist`` and should be run
periodically (e.g. via cron or a scheduled task) to prevent the
blacklist table from growing indefinitely.

Usage::

    python manage.py cleanup_expired_tokens
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.management.commands import (
    flushexpiredtokens,
)


class Command(BaseCommand):
    help = "Delete expired tokens from the blacklist"

    def handle(self, *args: object, **options: object) -> None:
        self.stdout.write("Flushing expired blacklisted tokens...")
        flushexpiredtokens.Command().handle(*args, **options)
        self.stdout.write(self.style.SUCCESS("Done."))
