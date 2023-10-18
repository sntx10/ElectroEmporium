from django.core.mail import send_mail
from decouple import config
from config.celery import app


@app.task
def send_confirm_link(email, confirm_code):
    full_link = f'http://{config("ALLOWED_HOSTS").split(",")[1]}:{config("MAIN_PORT")}/api/v1/order/confirm/{confirm_code}/'
    send_mail(
        'Ссылка для подтверждение заказа',
        full_link,
        config('EMAIL_HOST_USER'),
        [email]
    )