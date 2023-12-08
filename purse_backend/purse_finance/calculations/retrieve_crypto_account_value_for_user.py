from django.contrib.auth import get_user_model
from django.db import transaction

from purse_core.base_task import BaseTask
from purse_core.exceptions import PlaidServiceException
from purse_finance.models import CryptoAccount



class RetrieveCryptoAccountValueForUser(BaseTask):
    """
        Retrieve and update the value of crypto accounts for all crypto accounts of user
    """

    User = get_user_model()

    def run(self, user_id, auto_save=True, *args, **kwargs):

        with transaction.atomic():

            user = self.User.objects.get(id=user_id)
            try:
                for crypto_account in user.cryptoaccount_set.all():
                    value, _ = crypto_account.get_value()
                    self.results[crypto_account.id].append(value)
                return self.results
            except CryptoAccount.DoesNotExist as e:
                raise e
            except PlaidServiceException as e:
                raise e            