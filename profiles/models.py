from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    first_name = models.CharField(max_length=20, default="")

    def __str__(self):
        return f'{self.user.username}'
    # my_location = models.CharField(max_length=20, default="")
# birth_date = models.DateField(auto_now=False, auto_now_add=False, default=2000-4-9)
# my_location = models.CharField(max_length=50)
# If the user gets deleted, then this profile gets deleted to
# author = models.ForeignKey(User, on_delete=models.CASCADE)
