#!/bin/sh
cd /app

caddy start --config /app/Caddyfile --adapter caddyfile

crond

cd /app/backend

python manage.py migrate 

python cli/create_init_user.py

python manage.py crontab add

python manage.py runserver 0.0.0.0:8000

