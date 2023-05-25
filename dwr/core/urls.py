from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import SubscriptionListViews, CityDetailView, AboutView, UserRegisterView

urlpatterns = [
    path('', SubscriptionListViews.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<slug:slug>/', CityDetailView.as_view(), name='city_detail'),
]
