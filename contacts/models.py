from django.db import models
from datetime import datetime

class Contact(models.Model):
    # advertisement = models.CharField(max_length=200)
    recipient_id = models.IntegerField()
    # name = models.CharField(max_length=200)
    # email = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    sender_id = models.IntegerField()
    def __str__(self):
        return self.message