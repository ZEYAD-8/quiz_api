#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
