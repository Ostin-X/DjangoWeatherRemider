from rest_framework import serializers

from .models import City, Country


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # fields = '__all__'
        fields = ('name', 'country', 'codename', 'weather_data',)
