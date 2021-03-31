from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
import shutil
from advertisements.models import Advertisement, Category, UserSavedAd
from advertisements.views import save_or_delete_ad

TEST_DIR = 'test_data'


class BaseTest(TestCase):
    def setUp(self):
        self.ads_url = '/advertisements/'
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
        image_path = 'l3.jpg'
        self.ad = {
            'title': 'title1',
            'description': 'loremipsum',
            'price': 100,
            'category': 1,
            'latitude': 56.000224,
            'longitude': 34.456789,
            'image_main': SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                             content_type='image/jpg')
        }
        self.ad2 = {
            'title': 'title2',
            'description': 'loremipsum2',
            'price': 100,
            'category': 1,
            'latitude': 56.000224,
            'longitude': 34.456789,
            'image_main': SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                             content_type='image/jpg')
        }

        Category.objects.create(name='test')

        self.factory = RequestFactory()

        return super().setUp()


class TestViews(BaseTest):

    def test_can_view_all_ads(self):
        response = self.client.get(self.ads_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'advertisements/ads.html')

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_logged_in_user_can_post_add(self):
        self.client.login(username='user', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.user.username,
                          'password': self.user.password}, format='text/html')
        response = self.client.post(self.ad_create_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.__contains__('ad'))
        self.assertIsNotNone(Advertisement.objects.all().get(title=self.ad.get("title")))

    def test_logged_out_user_cant_post_ad_and_get_redirected_to_login(self):
        response = self.client.post(self.ad_create_url, self.ad, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.__contains__('login'))

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_logged_in_user_can_save_ad(self):
        self.client.login(username='user', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.user.username,
                          'password': self.user.password}, format='text/html')
        response = self.client.post(self.ad_create_url, self.ad2, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.__contains__('ad'))
        ad = Advertisement.objects.all().get(title=self.ad2.get("title"))
        self.assertIsNotNone(ad)

        # login user2
        self.client.login(username='user2', password='12345')
        self.client.post(self.authentication_url,
                         {'username': self.user2.username,
                          'password': self.user2.password}, format='text/html')

        request = self.factory.get('/advertisements/ad/' + str(ad.id) + '/')
        request.user = self.user2
        try:
            save_or_delete_ad(request, ad.id)
        except:
            # exception is thrown due to redirection to previous page, not relevant
            pass
        self.assertIsNotNone(UserSavedAd.objects.get(user=self.user2, ad=ad))

    # to remove the `TEST_DIR` folder at the
    # end of tests
    def tearDown(self):
        print(
        "\nDeleting temporary files...\n")
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
