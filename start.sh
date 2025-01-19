#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata dump.json
gunicorn quiz_api.wsgi:application --bind 0.0.0.0:$PORT
