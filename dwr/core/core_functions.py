from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

import environ

env = environ.Env()
environ.Env.read_env()


def get_weather(city):
    owm = OWM(env('OWM_API_KEY'))
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(city)
    # observation = mgr.weather_at_coords(lat, lon)

    w = observation.weather
    return w.temperature('celsius')['temp']

    w.detailed_status  # 'clouds'
    w.wind()  # {'speed': 4.6, 'deg': 330}
    w.humidity  # 87
    w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    w.rain  # {}
    w.heat_index  # None
    w.clouds  # 75


def get_weather_to_queryset(queryset):
    for sub in queryset:
        sub.weather_data = round(get_weather(sub.name))
        sub.save(update_fields=['weather_data'])
    return queryset
