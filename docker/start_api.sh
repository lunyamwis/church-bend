#!/bin/bash

source /root/.local/share/virtualenvs/brooks-insurance-*/bin/activate

echo "<<<<<<<< Collect Staticfiles>>>>>>>>>"
python manage.py collectstatic --noinput


sleep 14
echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
# Run database migrations
python manage.py migrate &

sleep 5
echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>>"
echo " "

echo " "
echo "<<<<<<<<<<<<<<<<<<<< START Celery >>>>>>>>>>>>>>>>>>>>>>>>"

# # start Celery worker
celery -A app worker -l info --pool=gevent --concurrency=1000 &

# # start celery beat
# celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info &

sleep 5
echo "<<<<<<<<<<<<<<<<<<<< START API >>>>>>>>>>>>>>>>>>>>>>>>"
# python manage.py runserver 0.0.0.0:8000
# Start the API with gunicorn
gunicorn --bind 0.0.0.0:8000 app.wsgi --reload --access-logfile '-' --workers=2
