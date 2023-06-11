from django.db import transaction

from purse_core.base_task import BaseTask
from purse_core.exceptions import PlaidServiceException
from purse_finance.models import PlaidAccount



class RetrievePlaidAccountBalance(BaseTask):
    """
    
        Retrieve the account balance from plaid for an account and save this data
    """

    def run(self, plaid_account_id, auto_save=True, *args, **kwargs):

        with transaction.atomic():
            try:
                plaid_account = PlaidAccount.objects.get(id=plaid_account_id)
                account_data, last_update = plaid_account.get_account_data_by_account()
                current_balance = account_data.get("current_balance")

                return {
                    "current_balance": current_balance,
                    "last_update": last_update
                }
            except PlaidAccount.DoesNotExist as e:
                raise e
            except PlaidServiceException as e:
                raise e            