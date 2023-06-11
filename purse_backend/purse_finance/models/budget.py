from django.db import models
from purse_auth.models import User


class Budget(models.Model):

    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)