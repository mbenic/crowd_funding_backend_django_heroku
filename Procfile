release: python manage.py migrate
web: gunicorn crowdfunding.wsgi:application --log-file -