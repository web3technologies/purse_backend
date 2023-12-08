from django.contrib.auth import get_user_model

from purse_core.base_task import BaseTask
from purse_core.exceptions import PlaidServiceException

from purse_finance.models import PlaidAccount


User = get_user_model()


class RetrievePlaidAccountTransactionsForUser(BaseTask):
    
    def run(self, user_id, *args, **kwargs):
        user = User.objects.prefetch_related("plaidaccount_set").get(id=user_id)
        try:
            for plaid_account in user.plaidaccount_set.all():
                transactions = plaid_account.get_transactions()
                self.results[plaid_account.id].append(transactions)
        except PlaidAccount.DoesNotExist as e:
            raise e
        except PlaidServiceException as e:
            raise e
        return self.results