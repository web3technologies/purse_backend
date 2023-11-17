from django.db import models
from django.utils import timezone

from purse_finance.models import PlaidAccount


class PlaidTransaction(models.Model):
    
    ammount = models.DecimalField(decimal_places=5, max_digits=100)
    date = models.DateField(default=timezone.now)
    name = models.CharField(blank=True, default="", max_length=255)
    merchant_name = models.CharField(blank=True, default="", max_length=255)
    is_pending = models.BooleanField(default=True)
    
    category_id = models.CharField(max_length=255, blank=True, default="")
    transaction_id = models.CharField(max_length=255, blank=True, default="")
    
    plaid_account = models.ForeignKey(PlaidAccount, null=True, on_delete=models.SET_NULL)
    
    ##internal fields
    date_retrieved = models.DateTimeField(default=timezone.now)
    is_reviewd = models.BooleanField(default=False)
    # internal_category = models.ForeignKey()