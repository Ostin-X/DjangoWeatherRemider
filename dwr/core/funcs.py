import environ
from pyowm import OWM
from django.core.mail import EmailMessage

from core.models import Subscription, User

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


def send_email(time_period):
    queryset = Subscription.objects.filter(time_period=time_period)
    user_list = queryset.distinct('user').values_list('user', flat=True)
    for user in user_list:
        mail_subject = 'Your weather info'
        message = f'Your weather info\n'
        for sub in queryset.filter(user=user):
            message += f'{sub.city.name} is {sub.city.weather_data} \n'
        to_email = User.objects.get(id=user).email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
    return 'OK'


def update_weather_sub_queryset(queryset):
    for sub in queryset:
        sub.city.weather_data = get_weather(sub.city.name, False)
        sub.city.save(update_fields=['weather_data'])


def update_weather_city_queryset(queryset):
    for city in queryset:
        city.weather_data = get_weather(city.name, False)
        city.save(update_fields=['weather_data'])
