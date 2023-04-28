import requests
from geopy.geocoders import Nominatim

print(Nominatim().geocode('Київ,  Україна').latitude)


# api_response = requests.get('http://127.0.0.1:8000/api/v1/city_list/')
# print(api_response.status_code)
# print(api_response.json())


# lat = 50.4501
# lon = 30.5234
# api_key = '0256f4d68991c093cd8e1bf65f5ffcb4'
# api_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
# print(api_response.json())
