from django.db import models
from django.contrib.auth.models import User

from advertisements.models import Advertisement, UserSavedAd


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_images")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=63.446827)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=10.421906)
    is_advertiser = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'
