from django.db import models
from django.utils import timezone

from purse_catalog.models import PlaidTransactionCategory
from purse_finance.models import PlaidAccount


class PlaidTransaction(models.Model):
    
    amount = models.DecimalField(decimal_places=5, max_digits=100)
    date = models.DateField(default=timezone.now)
    name = models.CharField(blank=True, default="", max_length=255)
    merchant_name = models.CharField(max_length=255, null=True, default=None)
    is_pending = models.BooleanField(default=True)
    
    category = models.ForeignKey(PlaidTransactionCategory, null=True, default=None, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(max_length=255, unique=True)
    
    plaid_account = models.ForeignKey(PlaidAccount, null=True, on_delete=models.SET_NULL)
    
    ##internal fields
    date_retrieved = models.DateTimeField(default=timezone.now)
    is_saved = models.BooleanField(default=False)
    is_income = models.BooleanField(null=True, default=None)
    # internal_category = models.ForeignKey() 