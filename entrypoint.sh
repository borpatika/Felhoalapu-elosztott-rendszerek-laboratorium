#!/bin/bash
set -e

mkdir -p /tmp/media  # itt működni fog
chmod -R 777 /tmp/media

echo "Running migrations..."
python manage.py migrate --noinput

exec "$@"
