from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images/categories')

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_main = models.ImageField(upload_to='images/advertisements')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=63.446827)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=10.421906)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING, related_name='advertisement')

    def get_absolute_url(self):
        return reverse('ad-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ": NOK" + str(self.price)


class UserSavedAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # When was this relationship established

    class Meta:
        unique_together = (('user', 'ad'))

    def __str__(self):
        return str(self.user) + "--" + str(self.ad)