from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.db.models import SET_NULL

from advertisements.models import Advertisement


class Contact(models.Model):
    recipient = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name='recipient_id')
    sender = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name='sender_id')
    advertisement = models.ForeignKey(Advertisement, null=True, on_delete=SET_NULL)
    message = models.TextField(blank=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, blank=True)
    message_read = models.BooleanField(default=False)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        first_part, second_part = 'Deleted user', 'Deleted user'
        if self.sender:
            first_part = self.sender.username
        if self.recipient:
            second_part = self.recipient.username
        return first_part + " --> " + second_part
