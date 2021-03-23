from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse, reverse_lazy


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_images/default.jpg", upload_to="profile_images")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=63.446827)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=10.421906)

    def __str__(self):
        return f'{self.user.username}'


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks", default="profile_username")
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(max_length=500)
    published = models.DateTimeField(default=timezone.now)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)

    # Dette er hva som vises i admin-panelet
    def __str__(self):
        return '%s - %s' % (self.author, self.rating)

    def get_absolute_url(self):
        return reverse('feedback', args=(str(self.id)))


