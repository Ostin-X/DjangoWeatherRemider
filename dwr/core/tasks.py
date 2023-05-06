from celery import shared_task

from pyowm import OWM
import environ
from .models import Subscription, City

env = environ.Env()
environ.Env.read_env()

owm = OWM(env('OWM_API_KEY'))
mgr = owm.weather_manager()


def get_weather(city, spoof=False):
    print(city)
    if spoof:
        from datetime import datetime
        return datetime.now()
    else:
        observation = mgr.weather_at_place(city)

    # observation = mgr.weather_at_coords(lat, lon)

    w = observation.weather
    return w.temperature('celsius')['temp']

    # w.detailed_status  # 'clouds'
    # w.wind()  # {'speed': 4.6, 'deg': 330}
    # w.humidity  # 87
    # w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    # w.rain  # {}
    # w.heat_index  # None
    # w.clouds  # 75


def update_weather_sub_queryset(queryset):
    for sub in queryset:
        sub.city.weather_data = get_weather(sub.city.name, True)
        sub.city.save(update_fields=['weather_data'])


def update_weather_city_queryset(queryset):
    for city in queryset:
        city.weather_data = get_weather(city.name, True)
        city.save(update_fields=['weather_data'])


@shared_task
def update_subscriptions_weather_data():
    queryset = Subscription.objects.all()
    update_weather_sub_queryset(queryset)
    return 'Weather data updated'


@shared_task
def send_1h_email_task():
    queryset = Subscription.objects.filter(time_period=1)
    return 'OK'


@shared_task
def send_3h_email_task():
    queryset = Subscription.objects.filter(time_period=3)
    return 'OK'


@shared_task
def send_6h_email_task():
    queryset = Subscription.objects.filter(time_period=6)
    return 'OK'


@shared_task
def send_12h_email_task():
    queryset = Subscription.objects.filter(time_period=12)
    return 'OK'
