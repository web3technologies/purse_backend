from django.db import models

from purse_catalog.models import PlaidTransactionSubCategory


class PlaidTransactionCategory(models.Model):
    
    plaid_category_id = models.IntegerField(unique=True)
    group = models.CharField(max_length=255)
    subcategories = models.ManyToManyField(PlaidTransactionSubCategory)

