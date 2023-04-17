from django.urls import path
from .views_api import CityAPIList

urlpatterns = [
    path('city_list/', CityAPIList.as_view(), name='city_list'),
    # path('city_list/<int:pk>/', CityAPIList.as_view(), name='city_list'),
]
