from django.utils import timezone
from django.db.models import Q
from django.db import models
from profiles.models import Profile


class Reklame(models.Model):
    text = models.CharField(max_length=64, blank=True)
    banner = models.ImageField(upload_to='images/reklame')
    advertiser = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                   limit_choices_to=Q(is_advertiser=True))
    published = models.DateTimeField(default=timezone.now)
