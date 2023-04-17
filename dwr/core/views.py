from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .core_functions import get_weather_to_queryset
from .models import City


def about(request):
    return render(request, 'core/about.html')


class SubscriptionListViews(ListView):
    model = City
    allow_empty = True
    template_name = 'core/index.html'
    context_object_name = 'cities'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_add = {
            'title': 'DWR Core App',
        }
        return {**context, **context_add}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = City.objects.filter(subs__user=self.request.user)
        else:
            queryset = City.objects.order_by('?')[:9]
        queryset = get_weather_to_queryset(queryset)
        return queryset


class CityDetailView(DetailView):
    model = City
    template_name = 'core/city_detail.html'
    context_object_name = 'city'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'DWR Core App'
        return context
