from django.contrib import admin

from .models import City, Subscription


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('id', 'name', 'country', 'codename')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'country', 'codename')

    ordering = ('name',)
    prepopulated_fields = {'slug': ('name', 'country')}


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ('id', 'user', 'city', 'is_active', 'time_period')
    list_display_links = ('id', 'city')
    search_fields = ('user', 'city')
    list_editable = ('is_active', 'time_period')

    ordering = ('user', 'city')


admin.site.register(City, CityAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
