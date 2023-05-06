from celery import shared_task

from pyowm import OWM
import environ
from .models import Subscription, City

env = environ.Env()
environ.Env.read_env()

owm = OWM(env('OWM_API_KEY'))
mgr = owm.weather_manager()


def get_weather(city):
    # owm = OWM(env('OWM_API_KEY'))
    # mgr = owm.weather_manager()

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


@shared_task
def update_subscriptions_weather_data():
    city_query = Subscription.objects.all().values('city')
    city_objects = City.objects.filter(id__in=city_query)
    for city in city_objects:
        print(f'---{city}---, ---{city.weather_data}---')
        city.weather_data = 4444
        # city.weather_data = get_weather(city.name)
        print(f'---{city}---, ---{city.weather_data}---')
        city.save(update_fields=['weather_data'])
        print(f'---{city}---, ---{city.weather_data}---')


@shared_task
def send_4h_email_task():
    queryset = Subscription.objects.filter(time_period=4)
    return 'OK'


@shared_task
def send_8h_email_task():
    queryset = Subscription.objects.filter(time_period__in=[4, 8])
    return 'OK'


@shared_task
def send_12h_email_task():
    print('32g;sndfjkbnfgb')
    queryset = Subscription.objects.filter(time_period__in=[4, 8, 12])
    print('Send 12h email')
    print(Subscription.objects.filter(time_period=4))
    print(Subscription.objects.filter(time_period__in=[4, 8]))
    print(Subscription.objects.filter(time_period__in=[4, 8, 12]))
    for subscription in queryset:
        print(subscription.user)
        print(subscription.city)
        print(subscription.time_period)
        print('---------------------')
    return 'OK'


@shared_task
def send_24h_email_task():
    print('32g;sndfjkbnfgb')
