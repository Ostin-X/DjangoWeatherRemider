from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import City, Country, Subscription


class CitySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all())

    class Meta:
        model = City
        # fields = '__all__'
        fields = ('name', 'country', 'codename', 'weather_data',)


class CaseInsensitiveSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field + '__iexact': data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=str(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class SubscriptionSerializer(serializers.ModelSerializer):
    city = CaseInsensitiveSlugRelatedField(slug_field='name', queryset=City.objects.all())

    # city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('user', 'city', 'is_active', 'time_period', 'weather_data',)

    # user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print(data)
    #     data['city'] = data['city'].title()
    #     return data
