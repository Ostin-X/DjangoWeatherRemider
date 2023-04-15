from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Subscription, City


def about(request):
    return render(request, 'core/about.html')


class SubscriptionListViews(ListView):
    model = Subscription
    allow_empty = True
    template_name = 'core/index.html'
    context_object_name = 'subs'

    def get_context_data(self, **kwargs):
        print(self.request.user.subs.last())
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.request.user} - DWR Sub List'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.subs.all()
        else:
            return Subscription.objects.order_by('?')[:3]


class CityDetailView(DetailView):
    model = City
    template_name = 'core/city_detail.html'
    context_object_name = 'city'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'DWR Core App'
        return context
