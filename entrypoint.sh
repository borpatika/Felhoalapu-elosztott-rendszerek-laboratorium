#!/bin/bash

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Execute CMD
exec "$@"
