from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import City, Subscription
from .serializers import CitySerializer, SubscriptionSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'


# class CityAPIList(generics.ListCreateAPIView):
#     # queryset = City.objects.all()
#     serializer_class = CitySerializer
#
#     def get_queryset(self):
#         if not (slug := self.kwargs.get('slug')):
#             queryset = City.objects.all()
#         else:
#             queryset = City.objects.filter(slug=slug)
#         return queryset


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    lookup_field = 'slug'

    @action(methods=['get'], detail=False)
    def users(self, request):
        user = User.objects.all()
        return Response({'user': [i.username for i in user]})



# class SubscriptionAPIList(generics.ListCreateAPIView):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer
#
#     def post(self, request, *args, **kwargs):
#         request.data['city'] = request.data['city'].title()
#         return self.create(request, *args, **kwargs)
#
#     # def get_queryset(self):
#     #     # for development default user
#     #     # if (user := self.request.user).id is None:
#     #     #     user = User.objects.get(username='ostin')
#     #     queryset = Subscription.objects.filter(user=user, is_active=True)
#     #     return queryset
#
#
# class SubscriptionAPIUpdate(generics.UpdateAPIView):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer
#     lookup_field = 'slug'
