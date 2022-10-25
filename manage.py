#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import django
from django.core.cache import cache

ip = "127.0.0.1"
port = 80

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s - %(levelname)s]: %(message)s")


def init_on_CVM_server(exec_):
    # MySQL Database
    exec_([sys.argv[0], "makemigrations"])
    exec_([sys.argv[0], "migrate"])
    # Static Files Collect
    exec_([sys.argv[0], "collectstatic"])


if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWebsite.settings')
    django.setup()

    from applications import application

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if cache.get("start-application") is True:
        application.appHandler.run_app()
        logging.info(f"start server at process {os.getpid()}.")
    else:
        cache.set("start-application", True, timeout=10)
    execute_from_command_line(sys.argv if sys.argv[1:] else sys.argv + ["runserver", f"{ip}:{port}"])
