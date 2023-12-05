from django.db import transaction

from purse_core.base_task import BaseTask
from purse_core.exceptions import PlaidServiceException
from purse_finance.models import PlaidAccount



class RetrievePlaidAccountTransactions(BaseTask):
    """
        Retrieve the account balance from plaid for an account and save this data
    """

    def run(self, plaid_account_id, *args, start_date=None, end_date=None,offset=0,  **kwargs):

        with transaction.atomic():
            try:
                plaid_account = PlaidAccount.objects.get(id=plaid_account_id)
                transactions = plaid_account.get_transactions(
                                start_date=start_date,
                                end_date=end_date,
                                offset=offset
                )
                return transactions
            except PlaidAccount.DoesNotExist as e:
                raise e
            except PlaidServiceException as e:
                raise e            