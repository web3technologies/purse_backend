from django.db import models
from purse_auth.models import User



class NetWorth(models.Model):


    networth = models.CharField(max_length=255)
    cash = models.CharField(max_length=255, default=None, null=True)
    assets = models.CharField(max_length=255, default=None, null=True)
    debt = models.CharField(max_length=255, default=None, null=True) 

    date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)