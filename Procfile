web: gunicorn registration.wsgi:application --log-file -
web: python manage.py migrate && gunicorn registration.wsgi