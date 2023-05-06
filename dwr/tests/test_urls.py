import tempfile
from django.test import TestCase, override_settings, RequestFactory
from django.core.management import call_command
from django.urls import reverse

from unittest.mock import patch

from core.models import City, Country, Subscription, User
from .fixtures import test_temp, mock_get_weather
from dwr.settings import DATABASES


# @override_settings(MEDIA_ROOT=tempfile.mkdtemp(), DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
@patch('core.tasks.get_weather', mock_get_weather)
class TestUrlsClass(TestCase):
    def setUp(self):
        # see what is RequestFactory
        self.factory = RequestFactory()

        self.test_user = User.objects.create_user(username='testuser', email='12345@qwe.com', password='12345')
        call_command('fill_countries')
        filename = 'worldcities_tst.csv'
        call_command('fill_test_cities', filename=filename)
        Subscription.objects.create(user=User.objects.get(username='testuser'), city=City.objects.get(name='Delhi'))

    def test_subs_list(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTemplateNotUsed(response, 'core/city_detail.html')
        self.assertEqual(len(response.context_data['object_list']), 9)
        # self.assertEqual(response.context_data['object_list'][0].weather_data, test_temp)

    def test_subs_list_logged_in(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTemplateNotUsed(response, 'core/city_detail.html')
        self.assertEqual(len(response.context_data['object_list']), 1)
        # self.assertEqual(response.context_data['object_list'][0].weather_data, test_temp)
        self.assertEqual(response.context_data['object_list'][0], City.objects.get(name='Delhi'))
        self.assertNotEquals(response.context_data['object_list'][0], City.objects.get(name='Beijing'))

    def test_city_view(self):
        response = self.client.get(reverse('city_detail', kwargs={'slug': 'delhiin'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/city_detail.html')
        self.assertTemplateNotUsed(response, 'core/index.html')
        self.assertEqual(response.context_data['object'], City.objects.get(name='Delhi'))
        self.assertEqual(response.context_data['object'].country, Country.objects.get(name='India'))
        # self.assertEqual(response.context_data['object'].weather_data, test_temp)
