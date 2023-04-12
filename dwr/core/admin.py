from django.contrib import admin

from .models import City


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('id', 'name', 'country', 'codename')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'country', 'codename')
    # list_editable = ('country', 'codename')

    ordering = ('name',)
    # list_filter = ('is_invisible',)
    # prepopulated_fields = {'slug': ('name',)}


admin.site.register(City, CityAdmin)
