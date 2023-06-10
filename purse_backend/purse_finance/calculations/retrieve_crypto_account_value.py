from django.db import transaction

from purse_core.base_task import BaseTask
from purse_core.exceptions import PlaidServiceException
from purse_finance.models import CryptoAccount



class RetrieveCryptoAccountValue(BaseTask):
    """
        Retrieve and update the value of a specific crypto account
    """

    def run(self, crypto_account_id, auto_save=True, *args, **kwargs):

        with transaction.atomic():
            try:
                crypto_account = CryptoAccount.objects.get(id=crypto_account_id)
                value, last_update = crypto_account.get_value()
                self.results[crypto_account.id].append(value)
                return {
                    'value': value,
                    "last_update": last_update
                }
            except CryptoAccount.DoesNotExist as e:
                raise e
            except PlaidServiceException as e:
                raise e            