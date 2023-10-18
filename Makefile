run:
	./manage.py runserver
migrate:
	./manage.py makemigrations
	./manage.py migrate
celery:
	celery -A config worker -l debug
beat:
	celery -A config beat
user:
	./manage.py createsuperuser
ngrok:
	ngrok http 8000
