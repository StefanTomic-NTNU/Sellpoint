from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.authentication_url = reverse('login')
        self.logout_url = reverse('logout')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.user = {
            'email': 'test@gmail.com',
            'username': 'test',
            'password': 'Rfe4433SFd',
            'password2': 'Rfe4433SFd'
        }
        return super().setUp()


class RegisterTest(BaseTest):

    def test_can_view_registration_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'profiles/register.html')

    def test_can_register_and_authenticate_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.authentication_url,
                                   {'username': 'test', 'password': 'Rfe4433SFd'}, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_page_redirect_if_user_logged_out(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.__contains__(self.login_url))

