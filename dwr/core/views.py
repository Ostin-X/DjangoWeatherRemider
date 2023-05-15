from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from .forms import CustomUserCreationForm
from .models import City
from .utils import DataMixin, NotLoggedAllow

from django.contrib.auth import login


@csrf_exempt
def webhook_current_datetime(request):
    from django.http import HttpResponse
    import datetime

    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        print(f'data - {data}')
        # process_webhook_request.delay(data)
        print(request.body)
        print(request.user)
        return HttpResponse(200, 'ok')
    else:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s. Not webhook time</body></html>" % now
        return HttpResponse(html)


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
