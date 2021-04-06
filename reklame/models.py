from django.utils import timezone
from django.db.models import Q
from django.db import models
from profiles.models import Profile


def one_week_hence():
    return timezone.now() + timezone.timedelta(weeks=1)


class Reklame(models.Model):
    text = models.CharField(max_length=64, blank=True)
    banner = models.ImageField(upload_to='images/reklame')
    advertiser = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                   limit_choices_to=Q(is_advertiser=True))
    published = models.DateTimeField(default=timezone.now)
    expired = models.DateTimeField(default=one_week_hence)


class RequestToBeAdvertiser(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, unique=True)
    sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.user.email


class RequestToRenewAbonement(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, unique=True)
    sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.user.email
