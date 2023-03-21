from django.core.management import BaseCommand
from os import system as call_commandline
from sys import exit


class Command(BaseCommand):
    help = 'start celery process by commandline'

    def handle(self, *args, **options):
        try:
            call_commandline("celery -A Deeptrain worker --loglevel=INFO -P eventlet")
        except KeyboardInterrupt:
            exit(0)
