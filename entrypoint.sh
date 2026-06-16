#!/bin/sh
set -e

python - <<'PYEOF'
import os
import sys
import time
import psycopg2

host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", "5432")
dbname = os.environ.get("POSTGRES_DB", "travel_diary")
user = os.environ.get("POSTGRES_USER", "travel_user")
password = os.environ.get("POSTGRES_PASSWORD", "")

print("Waiting for the database...")
for _ in range(30):
    try:
        psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password).close()
        print("Database is ready.")
        break
    except psycopg2.OperationalError:
        time.sleep(1)
else:
    print("Database did not become ready in time.", file=sys.stderr)
    sys.exit(1)
PYEOF

python manage.py migrate --noinput

if python - <<'PYEOF'
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travel_diary.settings")
django.setup()

from diary.models import Trip

sys.exit(0 if not Trip.objects.exists() else 1)
PYEOF
then
    echo "Seeding example trips..."
    cp -r /app/seed_media/. /app/media/
    python manage.py loaddata sample_data
fi

python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python - <<'PYEOF'
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travel_diary.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
PYEOF
fi

exec gunicorn travel_diary.wsgi:application --bind 0.0.0.0:8000 --workers 3
