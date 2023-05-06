from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, \
#     IsAuthenticated

from .permissions import IsAdminOrReadOnly, IsOwnerOrIsAdmin
from .models import City, Subscription, Country
from .serializers import CitySerializer, SubscriptionSerializer


class CityPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CityViewSet(viewsets.ModelViewSet):  # ReadOnlyModelViewSet
    serializer_class = CitySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    # pagination_class = CityPagination

    def get_queryset(self):
        # country = (self.request.GET.get('country'))
        # try:
        if country := (self.request.GET.get('country')):
            return City.objects.filter(country__slug=country.lower())
        # except AttributeError:
        else:
            return City.objects.all()

    @action(methods=['get'], detail=False)
    def countries(self):
        country = Country.objects.all()
        return Response({'country': [i.name for i in country]})


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrIsAdmin]

    def get_queryset(self):
        if (user_object := self.request.user).is_staff:
            queryset = Subscription.objects.all()
        else:
            queryset = Subscription.objects.filter(user=user_object)
        return queryset

    @action(methods=['get'], detail=False)
    def users(self):
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
