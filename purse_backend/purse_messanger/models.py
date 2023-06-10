from django.db import models
from django.conf import settings

from purse_core.settings.choices import MESSAGE_CHOICE_TYPES


class Message(models.Model):

    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255, choices=MESSAGE_CHOICE_TYPES)
    message_id = models.CharField(max_length=255, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

