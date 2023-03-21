#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import django
import redis

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s]: %(message)s",
)


def _init_website():
    try:
        django.setup()
        from applications.application import appManager
        appManager.setup_app()
    except redis.exceptions.ConnectionError as e:
        raise ConnectionError("Redis was un-connectable.") from e


def exec_website() -> 0:
    _init_website()

    exec_line = sys.argv if sys.argv[1:] \
        else sys.argv + ["runserver", f"{settings.DEFAULT_HOST}:{settings.DEFAULT_PORT}"]
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    return int(not not execute_from_command_line(exec_line))


if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Deeptrain.settings')
    from Deeptrain import settings
    settings.IS_DEPLOYED = False

    sys.exit(exec_website())
