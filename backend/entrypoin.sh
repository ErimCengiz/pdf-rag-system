#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --workers=1 \
    --threads=1 \
    --timeout=0 \
    --bind=0.0.0.0:8000
