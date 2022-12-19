#!/bin/bash
export PYTHONOPTIMIZE=1
gunicorn DjangoWebsite.wsgi:application -c gunicorn.conf.py
