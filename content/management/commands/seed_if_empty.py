"""
content/management/commands/seed_if_empty.py

Loads data/seed.json ONLY if the database has no chapters.
Safe to run on every deploy — skips if data already exists.

Usage:
  python manage.py seed_if_empty
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from content.models import Chapter


class Command(BaseCommand):
    help = 'Load seed.json fixture if the database is empty (no chapters).'

    def handle(self, *args, **options):
        if Chapter.objects.exists():
            self.stdout.write(self.style.SUCCESS(
                '[seed_if_empty] Chapters already exist — skipping.'))
            return

        fixture_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))),
            'data', 'seed.json'
        )

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.WARNING(
                f'[seed_if_empty] Fixture not found at {fixture_path} — skipping.'))
            return

        self.stdout.write('[seed_if_empty] Database is empty — loading seed data...')
        call_command('loaddata', fixture_path, verbosity=1)
        self.stdout.write(self.style.SUCCESS(
            '[seed_if_empty] Seed data loaded successfully!'))
