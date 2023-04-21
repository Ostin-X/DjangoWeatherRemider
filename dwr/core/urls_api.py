from django.urls import path, include
from rest_framework import routers

from .views_api import CityViewSet, SubscriptionViewSet

# router = routers.SimpleRouter()
router = routers.DefaultRouter()
router.register(r'city', CityViewSet, basename='city')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),

    # path('city/', CityAPIList.as_view()),
    # path('city/<slug:slug>/', CityAPIList.as_view()),
    # path('subscription_list/', SubscriptionViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('subscription_update/<str:slug>/', SubscriptionViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
]
