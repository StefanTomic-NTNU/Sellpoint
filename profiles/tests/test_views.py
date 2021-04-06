from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test.client import Client
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test',
            password='Rfe4433SFd'
        )
        self.user.set_password('tullepassord')
        self.user.save()

        self.register_url = reverse('register')
        self.authentication_url = reverse('login')
        self.profile_delete_url = reverse('profile-delete')
        self.profile_detail_url = reverse('profile-detail', args=[self.user.pk])
        return super().setUp()

    def test_can_view_profile_page(self):
         response = self.client.get(self.profile_detail_url)
    #    self.assertEquals(response.status_code, HTTPStatus.OK)
   #     self.assertTemplateUsed(response, 'profiles/profile_detail.html')

    def test_delete_own_user(self):
        c = Client()
        logged_in = c.login(username='test', password='tullepassord')
        self.assertTrue(User.objects.get(pk=self.user.pk))
        response = c.get(self.profile_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        with self.assertRaisesRegex(User.DoesNotExist, 'User matching query does not exist'):
            User.objects.get(pk=self.user.pk)
