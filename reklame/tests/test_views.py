from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
import shutil
from reklame.models import Reklame, RequestToBeAdvertiser, RequestToRenewAbonement

TEST_DIR = 'test_data'


class BaseTest(TestCase):
    def setUp(self):
        self.create_reklame_url = reverse('reklame-create')
        self.become_advertiser_url = reverse('become-advertiser')
        self.renew_subscription_url = reverse('renew-subscription')
        self.register_url = reverse('register')
        self.authentication_url = reverse('login')
        self.advertiser = User.objects.create(username='user', password='12345')
        self.advertiser.set_password('12345')
        self.advertiser.profile.is_advertiser = True
        self.advertiser.profile.reklame_limit = 3
        self.advertiser.save()
        self.not_advertiser = User.objects.create(username='user2', password='12345')
        self.not_advertiser.set_password('12345')
        self.not_advertiser.profile.is_advertiser
        self.not_advertiser.save()
        poster_path = 'l3.jpg'
        self.ad = {
            'banner': SimpleUploadedFile(name='test_image.jpg', content=open(poster_path, 'rb').read(),
                                             content_type='image/jpg')
        }
        return super().setUp()


class TestViews(BaseTest):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_logged_in_advertiser_can_post_reklame(self):
        self.client.login(username='user', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.advertiser.username,
                          'password': self.advertiser.password}, format='text/html')
        response = self.client.post(self.create_reklame_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIsNotNone(Reklame.objects.all().get(advertiser=self.advertiser.profile))

    def test_logged_in_user_can_send_request_to_become_advertiser(self):
        self.client.login(username='user2', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.not_advertiser.username,
                          'password': self.not_advertiser.password}, format='text/html')
        response = self.client.post(self.become_advertiser_url, {'author': self.not_advertiser.profile}, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIsNotNone(RequestToBeAdvertiser.objects.all().get(author=self.not_advertiser.profile))

    def test_avertiser_can_send_request_to_renew_abonement(self):
        self.advertiser.profile.reklame_limit = 0
        self.advertiser.save()
        self.client.login(username='user', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.advertiser.username,
                          'password': self.advertiser.password}, format='text/html')
        self.client.post(self.authentication_url,
                         {'username': self.advertiser.username,
                          'password': self.advertiser.password}, format='text/html')
        response = self.client.post(self.renew_subscription_url, {'author': self.advertiser.profile},
                                    format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIsNotNone(RequestToRenewAbonement.objects.all().get(author=self.advertiser.profile))

    # to remove the `TEST_DIR` folder at the
    # end of tests
    def tearDown(self):
        print(
        "\nDeleting temporary files...\n")
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
