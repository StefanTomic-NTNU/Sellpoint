from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_images")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=63.446827)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=10.421906)

    def __str__(self):
        return f'{self.user.username}'


class Feedback(models.Model):
    comment = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)

    # Dette er hva som vises i admin-panelet
    def __str__(self):
        return '%s - %s' % (self.author, self.rating)
