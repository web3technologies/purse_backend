from django.db import models
from django.utils import timezone

from plaid.exceptions import ApiException as PlaidApiException
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

from purse_auth.models import User
from purse_core.client import plaid_client
from purse_core.settings.choices import ITEM_STATUS_CHOICES
from purse_finance.mixins.plaid_exception import PlaidUtilityMixin
from purse_catalog.models import PlaidApiError


class Item(models.Model, PlaidUtilityMixin):

    access_token = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="ACTIVE", choices=ITEM_STATUS_CHOICES)
    plaid_internal_status = models.ForeignKey(PlaidApiError, on_delete=models.DO_NOTHING, default=1)

    plaid_item_id=models.CharField(max_length=255, null=True, default=None)
    institution=models.CharField(max_length=255, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.institution} -- {self.status}"


    def get_account_data(self):

        """
            Pass in the access_token for a plaid item and this will fetch all accounts for that token
        """

        from purse_finance.models.plaid_account import PlaidAccount

        try:
            request = AccountsBalanceGetRequest(access_token=self.access_token)
            response = plaid_client.accounts_balance_get(request)
            accounts = response['accounts']
            account_data = []

            for account in accounts:
                plaid_account_id = account.get("account_id")
                available_balance = account.get("balances").get("available")
                current_balance = account.get("balances").get("current")

                plaid_account = PlaidAccount.objects.get(plaid_account_id=plaid_account_id)
                plaid_account.available_balance = available_balance
                plaid_account.current_balance = current_balance
                plaid_account.last_update = timezone.now()
                plaid_account.save(update_fields=["current_balance", "available_balance", "last_update"])

                account_data.append(
                        {
                            "account_id": plaid_account_id,
                            "available_balance": available_balance,
                            "current_balance": current_balance,
                            "name": account.get("name"),
                            "official_name": account.get("official_name"),
                            "type": str(account.get("type"))
                        }
                )
            return account_data
        except PlaidApiException as e:
            self._handle_api_exception(exception=e, item=self)
            raise PlaidApiException(e)

    def get_transactions(self, start_date=None, end_date=None, serialize=True):
        
        options = TransactionsGetRequestOptions(offset=0)

        try:
            request = TransactionsGetRequest(
                access_token=self.access_token,
                start_date=start_date if start_date else self._calculate_start_date(),
                end_date=self.today if not end_date else end_date,
                options=options
            )
            response = plaid_client.transactions_get(request)
            transactions = response['transactions']

            if serialize:
                transactions = self._serialize_transaction_data(transactions)
            return transactions

        except PlaidApiException as e:
            self._handle_api_exception(exception=e, item=self)
            raise PlaidApiException(e)




