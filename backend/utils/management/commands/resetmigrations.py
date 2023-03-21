"""
Management utility to create administrators.
refer to django.contrib.auth.management - createsuperuser
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Delete all of the migration files and regenerate migration files'

    def handle(self, *args, **options):
        from DjangoWebsite.settings import INSTALLED_APPS

        print("  Delete Migrations:")
        for app in INSTALLED_APPS:
            migration_dir = os.path.join(os.path.join(*app.split(".")), 'migrations')
            if os.path.isdir(migration_dir):  # 本地app
                print(f"    -", app)
                for path in filter(os.path.isfile,
                                   [os.path.join(migration_dir, file)
                                    for file in set(os.listdir(migration_dir)) - {"__init__.py", "__pycache__"}
                                    if file.endswith(".py")]):
                    print("      ", path)
                    os.remove(path)

        print("\nMake Migrations:", end="\n  ")
        call_command("makemigrations")
