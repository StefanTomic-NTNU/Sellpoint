from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=63.446827)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=10.421906)
    # birth_date = models.DateField(auto_now=False, auto_now_add=False, default=2000-4-9)
    def __str__(self):
        return f'{self.user.username}'