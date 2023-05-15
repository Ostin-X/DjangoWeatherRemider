from celery import shared_task

from .funcs import update_weather_sub_queryset, send_email
from .models import Subscription


@shared_task
def update_subscriptions_weather_data():
    queryset = Subscription.objects.all()
    update_weather_sub_queryset(queryset)
    return 'Weather data updated'


@shared_task
def send_1h_email_task():
    send_email(1)
    return 'OK'


@shared_task
def send_3h_email_task():
    send_email(3)
    return 'OK'


@shared_task
def send_6h_email_task():
    send_email(6)
    return 'OK'


@shared_task
def send_12h_email_task():
    send_email(12)
    return 'OK'
