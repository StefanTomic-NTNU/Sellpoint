import shutil
from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from advertisements.models import Advertisement, Category
from contacts.models import Contact

TEST_DIR = 'test_data'


class BaseTest(TestCase):
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        self.user1 = User.objects.create(
            email='contact1@test.com',
            username='contact1_test',
            password='Rfe4433SFd'
        )
        self.user1.set_password('tullepassord')
        self.user1.save()

        self.user2 = User.objects.create(
            email='contact2@test.com',
            username='contact2_test',
            password='Rfe4433SFd'
        )
        self.user2.set_password('tullepassord')
        self.user2.save()

        self.category = Category.objects.create(
            name='Møbler',
            image=SimpleUploadedFile(name='test_image.jpg',
                                            content=open('l3.jpg', 'rb').read(),
                                            content_type='image/jpg'),
        )

        self.user1_ad = Advertisement.objects.create(
            title='Stol',
            description='Fin stol',
            price=1000,
            image_main=SimpleUploadedFile(name='test_image.jpg',
                                          content=open('l3.jpg', 'rb').read(),
                                          content_type='image/jpg'),
            author=self.user2,
            category=self.category
        )

        self.user2_ad = Advertisement.objects.create(
            title='Stol2',
            description = 'Fin stol',
            price = 1000,
            image_main = SimpleUploadedFile(name='test_image.jpg',
                                            content=open('l3.jpg', 'rb').read(),
                                            content_type='image/jpg'),
            author = self.user2,
            category = self.category
        )

        self.contact_user2_ad_url = reverse('contact', args=[self.user2_ad.pk])
        self.inbox_url = reverse('inbox')

        self.client.login(username='contact1_test', password='tullepassord')
        return super().setUp()


class TestViews(BaseTest):

    def test_can_send_message(self):
        message = {
            'message': 'Hei, dette er en test',
            'phone': '12312312',
            'email': 'contact1@test.com'
            }
        response = self.client.get(self.contact_user2_ad_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.contact_user2_ad_url, message, format='text/html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertEqual(response.url, reverse('advertisements'))

    def test_user_can_view_received_messages(self):
        message = 'tullemelding'
        contact = Contact.objects.create(
            recipient=self.user1,
            sender=self.user2,
            advertisement=self.user1_ad,
            message=message,
            email=self.user2.email,
            phone='12312311'
        )
        contact.save()
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_content = response.content.decode("utf-8")

        self.assertTrue(message in response_content)
        self.assertTrue(self.user2.username in response_content)
        self.assertTrue(self.user1_ad.title in response_content)

    def tearDown(self):
        """ Removes 'TEST_DIR' folder at the end of tests """
        print(
        "\nDeleting temporary files...\n")
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
