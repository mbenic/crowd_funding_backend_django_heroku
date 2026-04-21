release: python manage.py migrate && python manage.py seed
web: gunicorn crowdfunding.wsgi:application --log-file -