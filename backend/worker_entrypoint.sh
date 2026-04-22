#!/bin/bash
set -e

echo "=== Worker container starting ==="

python manage.py migrate --no-input
echo "=== Migrations complete ==="

echo "=== Starting cron scheduler ==="
exec supercronic /backend/crontab
