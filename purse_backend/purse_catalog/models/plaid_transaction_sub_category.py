from django.db import models


class PlaidTransactionSubCategory(models.Model):

    label = models.CharField(max_length=255, unique=True)
