#!/bin/sh

#./setup.sh

service cron start
mkdir log 2> /dev/null
rm -f log/places_cron.log
rm -f log/ladph_cron.log

python manage.py makemigrations places
python manage.py migrate

python manage.py crontab add
python manage.py crontab add
python manage.py crontab add

python manage.py runserver 0.0.0.0:8000
