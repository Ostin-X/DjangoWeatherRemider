from django.forms import model_to_dict
from rest_framework import generics

from .models import City, Country
from .serializers import CitySerializer


# class CityListApiView(APIView):
#     def get(self, request):
#         city = City.objects.all().values()
#         # serializer = CitySerializer(city, many=True)
#         return Response({'cities': list(city)})
#
#     def post(self, request):
#         post_new = City.objects.create(
#             name=request.data['name'],
#             country=Country.objects.get(name=request.data['country']),
#         )
#         return Response({'message': model_to_dict(post_new)})


class CityAPIList(generics.ListCreateAPIView):
    model = City
    serializer_class = CitySerializer

    # paginate_by = 10
    # paginate_by_param = 'page_size'
    # max_paginate_by = 100

    def get_queryset(self):
        return City.objects.all()

    def post(self, request, *args, **kwargs):
        new_country_pk = Country.objects.get(name=request.data['country']).pk
        request.data['country'] = new_country_pk
        return self.create(request, *args, **kwargs)
