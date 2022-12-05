#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import django
import redis
from django.core.cache import cache

ip = "127.0.0.1"
port = 8000

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s]: %(message)s",
)


def initialize_applications(run=False):
    django.setup()
    from applications import application
    application.appHandler.setup_app()
    logging.debug(f"Initialize applications successfully.")
    if run:
        if cache.get("start-application") is True:
            application.appHandler.run_app()
            logging.info(f"start server at process {os.getpid()}.")
        else:
            cache.set("start-application", True, timeout=10)


if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWebsite.settings')
    exec_line = sys.argv if sys.argv[1:] else sys.argv + ["runserver", f"{ip}:{port}"]
    try:
        initialize_applications(exec_line[1] == "runserver")
    except redis.exceptions.ConnectionError as e:
        raise ConnectionError("Redis was un-connectable.") from e

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(exec_line)
