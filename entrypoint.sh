#!/bin/bash
set -e

# Ensure media directory exists and is writable
mkdir -p /app/media
chmod -R 777 /app/media

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Execute CMD
exec "$@"
