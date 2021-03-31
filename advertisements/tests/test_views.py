from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from advertisements.models import Advertisement


class BaseTest(TestCase):
    def setUp(self):
        self.ads_url = '/advertisements/'
        self.ads_detail_url = reverse('ad-detail', args=['1'])
        self.save_ad_url = reverse('save-or-delete-ad', args=['1'])
        self.ad_create_url = reverse('ad-create')
        self.register_url = reverse('register')
        self.authentication_url = reverse('login')
        self.user = User.objects.create(username='user', password='12345')
        self.user.set_password('12345')
        self.user.save()
        self.user2 = User.objects.create(username='user2', password='12345')
        self.user2.set_password('12345')
        self.user2.save()
        self.ad = {
            'title': 'title1',
            'description': 'loremipsum',
        }
        self.ad2 = {
            'title': 'title2',
            'description': 'loremipsum2',
        }
        return super().setUp()


class TestViews(BaseTest):

    def test_can_view_all_ads(self):
        response = self.client.get(self.ads_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'advertisements/ads.html')

    def test_logged_in_user_can_post_add(self):
        self.client.login(username='user', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.user.username,
                          'password': self.user.password}, format='text/html')
        response = self.client.post(self.ad_create_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logged_out_user_cant_post_ad_and_get_redirected_to_login(self):
        response = self.client.post(self.ad_create_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.__contains__('login'))

