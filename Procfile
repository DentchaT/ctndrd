web: gunicorn appl.wsgi:application --log-file -
web: python manage.py migrate && gunicorn appl.wsgi