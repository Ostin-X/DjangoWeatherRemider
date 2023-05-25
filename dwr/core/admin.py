from django.contrib import admin

from .models import Country, City, Subscription


class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ('id', 'name', 'code')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'code')

    ordering = ('name',)


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('id', 'name', 'country', 'codename', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'codename')

    ordering = ('name',)


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ('id', 'user', 'city', 'is_active', 'time_period', 'webhook_url')
    list_display_links = ('id', 'city')
    search_fields = ('user', 'city')
    list_editable = ('is_active', 'time_period')

    ordering = ('user', 'city')


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
