from rest_framework.test import APIRequestFactory, APITestCase
from core.models import City, Subscription, User
from django.core.management import call_command


class TestApiClass(APITestCase):
    def setUp(self):
        # see what is APIRequestFactory
        self.factory = APIRequestFactory()

        self.test_user = User.objects.create_user(username='testuser', email='12345@qwe.com', password='12345')
        call_command('fill_countries')
        call_command('fill_test_cities')
        Subscription.objects.create(user=User.objects.get(username='testuser'), city=City.objects.get(name='Delhi'))

    def test_city_list_api_GET(self):
        response = self.client.get('/api/v1/city/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 17)
        self.assertIn('Bangkok', str(response.content))
        self.assertIn('Kolkata', str(response.content))
        self.assertNotIn('Kyiv', str(response.content))

    def test_city_china_api_GET(self):
        response = self.client.get('/api/v1/city/?country=China')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertNotIn('Bangkok', str(response.content))
        self.assertIn('Beijing', str(response.content))
        self.assertNotIn('Kyiv', str(response.content))

    def test_city_api_GET(self):
        response = self.client.get('/api/v1/city/beijingcn/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('Beijing', str(response.content))
        self.assertNotIn('Kyiv', str(response.content))
        self.assertNotIn('Bangkok', str(response.content))

    def test_subscription_api_GET_loggedout(self):
        response = self.client.get('/api/v1/subscription/')

        self.assertEqual(response.status_code, 403)

    def test_basic_login_api_POST(self):
        response = self.client.post('/api/v1/drf-auth/login/?next=/api/v1/city/',
                                    {'username': 'testuser', 'password': '12345'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Beijing', str(response.content))
        self.assertNotIn('Kyiv', str(response.content))
        self.assertIn('Bangkok', str(response.content))

    def test_JWT_api_POST(self):
        response = self.client.post('/api/v1/token/',
                                    {'username': 'testuser', 'password': '12345'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', str(response.content))
        self.assertIn('access', str(response.content))

        access_token = response.data['access']
        headers = {'Authorization': 'DWRBearer ' + access_token}
        response2 = self.client.get('/api/v1/subscription/', headers=headers)

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 1)
        self.assertIn('Delhi', str(response2.content))
        self.assertNotIn('Kyiv', str(response2.content))
        self.assertNotIn('Bangkok', str(response2.content))

    def test_JWT_api_POST_wrong_password(self):
        response = self.client.post('/api/v1/token/',
                                    {'username': 'testuser', 'password': 'wrong_password'})

        self.assertEqual(response.status_code, 401)

    def test_JWT_api_POST_wrong_username(self):
        response = self.client.post('/api/v1/token/',
                                    {'username': 'wrong_username', 'password': '12345'})

        self.assertEqual(response.status_code, 401)

    def test_JWT_api_POST_new_subscription(self):
        before_subs_count = Subscription.objects.count()
        response = self.client.post('/api/v1/token/',
                                    {'username': 'testuser', 'password': '12345'})
        access_token = response.data['access']
        headers = {'Authorization': 'DWRBearer ' + access_token}
        data = {'city': 'Bangkok'}

        response2 = self.client.post('/api/v1/subscription/', data=data, headers=headers)
        new_subs = Subscription.objects.all()

        self.assertEqual(response2.status_code, 201)
        self.assertEqual(new_subs.count(), before_subs_count + 1)
        self.assertIn('Bangkok', str(response2.content))
        self.assertNotIn('Beijing', str(response2.content))
        self.assertIn('Bangkok', new_subs.values_list('city__name', flat=True))
        self.assertNotIn('Beijing', new_subs.values_list('city__name', flat=True))

        response3 = self.client.get('/api/v1/subscription/', headers=headers)

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 2)
        self.assertIn('Delhi', str(response3.content))
        self.assertNotIn('Kyiv', str(response3.content))
        self.assertIn('Bangkok', str(response3.content))
        self.assertNotIn('Beijing', str(response3.content))

        data2 = {'city': 'Beijing'}
        # data2 = {'city': 'beiJing'}

        response4 = self.client.post('/api/v1/subscription/', data=data2, headers=headers)
        new_subs2 = Subscription.objects.all()

        # self.assertEqual(8, response4.data)
        self.assertEqual(response4.status_code, 201)
        self.assertEqual(new_subs2.count(), before_subs_count + 2)
        self.assertIn('Beijing', str(response4.content))
        self.assertIn('Beijing', new_subs.values_list('city__name', flat=True))

        response5 = self.client.get('/api/v1/subscription/', headers=headers)

        self.assertEqual(response5.status_code, 200)
        self.assertEqual(len(response5.data), 3)
        self.assertIn('Delhi', str(response5.content))
        self.assertNotIn('Kyiv', str(response5.content))
        self.assertIn('Bangkok', str(response5.content))
        self.assertIn('Beijing', str(response5.content))

    def test_JWT_api_POST_new_subscription_bad_city(self):
        before_subs_count = Subscription.objects.count()
        response = self.client.post('/api/v1/token/',
                                    {'username': 'testuser', 'password': '12345'})
        access_token = response.data['access']
        headers = {'Authorization': 'DWRBearer ' + access_token}
        data = {'city': 'moscow'}

        response2 = self.client.post('/api/v1/subscription/', data=data, headers=headers)
        new_subs = Subscription.objects.all()

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(new_subs.count(), before_subs_count)

    def test_1JWT_api_PUT_subscription(self):
        before_subs_count = Subscription.objects.count()
        first_sub_slug = Subscription.objects.filter(user__username='testuser')[0].slug

        response = self.client.post('/api/v1/token/', {'username': 'testuser', 'password': '12345'})
        access_token = response.data['access']
        headers = {'Authorization': 'DWRBearer ' + access_token}
        data = {'city': 'Beijing'}

        response2 = self.client.put(f'/api/v1/subscription/{first_sub_slug}/', data=data, headers=headers)
        new_subs = Subscription.objects.all()

        self.assertEqual(200, response2.status_code)
        self.assertEqual(new_subs.count(), before_subs_count)
        self.assertNotIn('Delhi', str(response2.content))
        self.assertIn('Beijing', str(response2.content))
        self.assertNotIn('Delhi', new_subs.values_list('city__name', flat=True))
        self.assertIn('Beijing', new_subs.values_list('city__name', flat=True))

    def test_JWT_api_PATCH_subscription(self):
        before_subs_count = Subscription.objects.count()
        first_sub = Subscription.objects.filter(user__username='testuser')[0]
        first_sub_slug = first_sub.slug
        first_sub_before_time_period = first_sub.time_period
        self.assertEqual(0, first_sub_before_time_period)

        response = self.client.post('/api/v1/token/', {'username': 'testuser', 'password': '12345'})
        access_token = response.data['access']
        headers = {'Authorization': 'DWRBearer ' + access_token}
        data = {'time_period': '4'}

        response2 = self.client.patch(f'/api/v1/subscription/{first_sub_slug}/', data=data, headers=headers)
        new_subs = Subscription.objects.all()
        new_sub = Subscription.objects.get(slug=first_sub_slug)

        self.assertEqual(200, response2.status_code)
        self.assertEqual(4, new_sub.time_period)
        self.assertEqual(new_subs.count(), before_subs_count)
        self.assertIn('Delhi', str(response2.content))
        self.assertIn('"time_period":4', str(response2.content))
        self.assertNotIn('Beijing', str(response2.content))
        self.assertIn('Delhi', new_subs.values_list('city__name', flat=True))
        self.assertNotIn('Beijing', new_subs.values_list('city__name', flat=True))

    def test_JWT_api_DELETE_subscription(self):
        before_subs_count = Subscription.objects.count()
        first_sub = Subscription.objects.filter(user__username='testuser')[0]
        first_sub_slug = first_sub.slug

        response = self.client.post('/api/v1/token/', {'username': 'testuser', 'password': '12345'})
        access_token = response.data['access']
        headers = {'Authorization': 'DWRBearer ' + access_token}
        # data = {'time_period': '4'}

        response2 = self.client.delete(f'/api/v1/subscription/{first_sub_slug}/', headers=headers)
        new_subs = Subscription.objects.all()

        self.assertEqual(204, response2.status_code)
        self.assertEqual(new_subs.count(), before_subs_count-1)
        self.assertNotIn('Delhi', str(response2.content))
        self.assertNotIn('Delhi', new_subs.values_list('city__name', flat=True))
