#!/bin/bash

SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-"mencigarzan@gmail.com"}

/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
