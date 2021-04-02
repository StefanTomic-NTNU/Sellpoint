from django.db import models
from datetime import datetime

class Contact(models.Model):
    recipient_id = models.IntegerField()
    advertisement_id = models.IntegerField(blank=True)
    message = models.TextField(blank=True)
    message_read = models.BooleanField(default=False)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    sender_id = models.IntegerField()
    def __str__(self):
        return self.message