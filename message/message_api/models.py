from django.db import models
from django.utils import timezone


class Messages(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    message = models.TextField()
    subject = models.TextField()
    creation_date = models.DateTimeField(max_length=60, default=timezone.now)
    message_read = models.BooleanField(default=False)
