from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views_api import CityViewSet, SubscriptionViewSet, WebhookView

# router = routers.SimpleRouter()
router = routers.DefaultRouter()
router.register(r'city', CityViewSet, basename='city')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),

    path('drf-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('webhook/', WebhookView.as_view(), name='webhook'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
