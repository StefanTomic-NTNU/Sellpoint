from http import HTTPStatus
from django.urls import reverse
from profiles.views import ProfileDetailView
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
        self.profile_detail_url = reverse('profile-detail', args=[self.user.pk])
        return super().setUp()

    def test_can_view_profile_page(self):
        response = self.client.get(self.profile_detail_url)
        self.assertEquals(response.status_code, HTTPStatus.OK)
