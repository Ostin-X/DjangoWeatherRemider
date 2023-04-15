from django.urls import path
from .views import about, SubscriptionListViews, CityDetailView

urlpatterns = [
    path('', SubscriptionListViews.as_view(), name='index'),
    path('about/', about, name='about'),
    path('<slug:slug>/', CityDetailView.as_view(), name='city_detail'),
]
