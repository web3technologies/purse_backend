from django.db import models
from django.contrib.auth import get_user_model

from purse_core.settings.choices import ACCOUNT_TYPE_CHOICES 


User = get_user_model()


class BaseAccount(models.Model):

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default="", choices=ACCOUNT_TYPE_CHOICES)
    
    class Meta:
        abstract = True