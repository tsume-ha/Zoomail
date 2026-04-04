#!/bin/sh
set -eu

python manage.py collectstatic --noinput
python manage.py migrate

exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --threads 2 \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --timeout 60