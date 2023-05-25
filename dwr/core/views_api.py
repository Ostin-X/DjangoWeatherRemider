from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated
# IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, \

from .permissions import IsAdminOrReadOnly, IsOwnerOrIsAdmin
from .models import City, Subscription, Country, User
from .serializers import CitySerializer, SubscriptionSerializer


class WebhookView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data_dict = request.data

        user_object = get_object_or_404(User, username=data_dict['user'])
        city_object = get_object_or_404(City, name=data_dict['city'].capitalize())
        webhook_url = data_dict['url']
        time_period = data_dict['time_period']

        if time_period not in [choice[0] for choice in Subscription.MY_CHOICES]:
            error_message = "Invalid time_period value provided. Must be (1,3,6,12)"
            return Response({"error": error_message}, status=400)

        try:
            sub, created = Subscription.objects.update_or_create(
                user=user_object,
                city=city_object,
                defaults={'webhook_url': webhook_url, 'time_period': time_period}
            )
        except Exception as e:
            return e

        if created:
            response_message = "Webhook created successfully"
        else:
            response_message = "Webhook updated successfully"

        return Response(response_message, status=201)


# class CityPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

class CityViewSet(viewsets.ModelViewSet):  # ReadOnlyModelViewSet
    serializer_class = CitySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    # pagination_class = CityPagination

    def get_queryset(self):
        if country := (self.request.GET.get('country')):
            return City.objects.filter(country__slug=country.lower())
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
