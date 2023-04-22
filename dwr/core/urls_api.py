from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views_api import CityViewSet, SubscriptionViewSet

# router = routers.SimpleRouter()
router = routers.DefaultRouter()
router.register(r'city', CityViewSet, basename='city')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),

    path('drf-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('city/', CityAPIList.as_view()),
    # path('city/<slug:slug>/', CityAPIList.as_view()),
    # path('subscription_list/', SubscriptionViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('subscription_update/<str:slug>/', SubscriptionViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
]
