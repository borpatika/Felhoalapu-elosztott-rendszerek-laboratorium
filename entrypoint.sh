#!/bin/bash
set -e

mkdir -p /app/media
chmod -R 777 /app/media

echo "Running migrations..."
python manage.py migrate --noinput

exec "$@"
