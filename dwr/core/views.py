from django.views.generic import ListView, DetailView, TemplateView, CreateView

from .core_functions import get_weather_to_queryset
from .forms import CustomUserCreationForm
from .models import City
from .utils import DataMixin, NotLoggedAllow


class UserRegisterView(NotLoggedAllow, DataMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = 'index'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context_add = self.get_user_context(title='Registration')
        return {**context, **context_add}


class SubscriptionListViews(DataMixin, ListView):
    model = City
    allow_empty = True
    template_name = 'core/index.html'
    context_object_name = 'cities'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SubscriptionListViews, self).get_context_data(**kwargs)
        context_add = self.get_user_context(title='My Cities')
        return {**context, **context_add}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = City.objects.filter(subs__user=self.request.user)
        else:
            queryset = City.objects.order_by('?')[:9]
        queryset = get_weather_to_queryset(queryset)
        return queryset


class CityDetailView(DataMixin, DetailView):
    model = City
    template_name = 'core/city_detail.html'
    context_object_name = 'city'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_add = self.get_user_context(title=self.object.name)
        return {**context, **context_add}


class AboutView(DataMixin, TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context_add = self.get_user_context(title='About')
        return {**context, **context_add}
