#!/bin/bash
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_PASSWORD=wkhWVx5k \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
python manage.py createsuperuser --noinput && \
python manage.py collectstatic --noinput && \
gunicorn --workers 2 cafeteriaServer.wsgi
