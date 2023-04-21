from django.contrib.auth.models import User
from rest_framework import serializers

from .models import City, Country, Subscription


class CitySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all())

    class Meta:
        model = City
        # fields = '__all__'
        fields = ('name', 'country', 'codename', 'weather_data',)


class SubscriptionSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    # for development default user
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                        default=User.objects.get(username='ostin'))

    class Meta:
        model = Subscription
        fields = ('user', 'city', 'is_active', 'time_period', 'weather_data',)
