#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

if [ "${LOAD_DEMO_DATA:-false}" = "true" ]; then
  python manage.py seed_demo
fi

if [ -n "${ADMIN_PASSWORD:-}" ]; then
  python manage.py ensure_admin
fi
