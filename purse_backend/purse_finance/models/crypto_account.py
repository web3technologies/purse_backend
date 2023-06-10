from django.db import models
from django.utils import timezone

from requests.exceptions import HTTPError

from purse_core.models import BaseAccount
from purse_core.services import crypto_service


class CryptoAccount(BaseAccount):

    ticker = models.CharField(max_length=255, default=None, null=True)
    amount = models.CharField(max_length=255)
    
    value = models.FloatField(default=0)
    last_update = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.ticker} -- {self.user}"
    

    def get_value(self):
        try:
            value = crypto_service.get_account_value(self.ticker, self.amount)
            self.value = value
            last_update = timezone.now()
            self.last_update = last_update
            self.save(update_fields=["value", "last_update"])
            return value, last_update
        except HTTPError as e:
            raise e