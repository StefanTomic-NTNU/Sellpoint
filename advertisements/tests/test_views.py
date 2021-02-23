from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from advertisements.models import Advertisement


class BaseTest(TestCase):
    def setUp(self):
        self.ads_url = '/advertisements/'
        self.ads_detail_url = reverse('ad-detail', args=['1'])
        self.ad_create_url = reverse('ad-create')
        self.register_url = reverse('register')
        self.authentication_url = reverse('login')
        self.user = {
            'email': 'test@gmail.com',
            'username': 'test',
            'password': 'Rfe4433SFd',
            'password2': 'Rfe4433SFd'
        }
        self.ad = {
            'title': 'title1',
            'description': 'loremipsum',
        }

        return super().setUp()


class TestViews(BaseTest):

    def __login__(self):
        self.client.post(self.register_url, self.user, format='text/html')
        self.client.post(self.authentication_url,
                         {'username': 'test', 'password': 'Rfe4433SFd'}, format='text/html')

    def test_can_view_all_ads(self):
        response = self.client.get(self.ads_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'advertisements/ads.html')

    def test_logged_in_user_can_post_add(self):
        self.__login__()
        response = self.client.post(self.ad_create_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_logged_out_user_cant_post_add_and_get_redirected_to_login(self):
        response = self.client.post(self.ad_create_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.__contains__('login'))


