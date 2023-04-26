from django.contrib.auth.mixins import UserPassesTestMixin

menu = [
    {"name": "My Cities", "url": "index"},
    {"name": "About", "url": "about"},
    {"name": "Admin", "url": "admin:index"},
]


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs
        user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu = menu[:1] + menu[2:-1]
        context['menu'] = user_menu
        return context


class NotLoggedAllow(UserPassesTestMixin):

    def test_func(self):
        return not self.request.user.is_authenticated
