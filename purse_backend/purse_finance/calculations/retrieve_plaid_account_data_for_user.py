from django.contrib.auth import get_user_model
from django.db import transaction

from purse_core.base_task import BaseTask
from purse_core.exceptions import PlaidServiceException
from purse_finance.models import PlaidAccount



class RetrievePlaidAccountBalanceForUser(BaseTask):
    """
    
        Retrieve the account balance from plaid for an account and save this data
    """

    User = get_user_model()

    def run(self, user_id, auto_save=True, *args, **kwargs):

        with transaction.atomic():

            user = self.User.objects.get(id=user_id)
            try:

                for item in user.item_set.all():
                    account_updates = item.get_account_data()
                    self.results[item.id].append(account_updates)
            
                return self.results
            except PlaidAccount.DoesNotExist as e:
                raise e
            except PlaidServiceException as e:
                raise e            