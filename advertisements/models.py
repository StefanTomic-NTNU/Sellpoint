from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Advertisement(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_main = models.ImageField(upload_to='images/advertisements')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.title +  ": $" + str(self.price)