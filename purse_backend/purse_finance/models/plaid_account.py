from django.db import models
from django.utils import timezone

from plaid.exceptions import ApiException as PlaidApiException
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_balance_get_request_options import AccountsBalanceGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

from purse_core.client import plaid_client
from purse_core.models import BaseAccount
from purse_core.settings.choices import PLAID_ACCOUNT_TYPE_CHOICES, PLAID_ACCOUNT_STATUS_CHOICES
from purse_finance.mixins.plaid_exception import PlaidUtilityMixin
from purse_finance.models import Item



class PlaidAccount(BaseAccount, PlaidUtilityMixin):

    account_type = models.CharField(max_length=255, default="",  choices=PLAID_ACCOUNT_TYPE_CHOICES)  # crypto
    plaid_account_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=PLAID_ACCOUNT_STATUS_CHOICES)

    available_balance = models.FloatField(default=None, null=True)
    current_balance = models.FloatField(default=None, null=True)
    last_update = models.DateTimeField(default=timezone.now)

    item = models.ForeignKey(Item, default=None, null=True, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.user.email} -- {self.name} -- {self.item.institution if self.item else ''} -- {self.plaid_account_id} -- {self.status}"


    def get_account_data_by_account(self):
        """
            then it will fetch the data from plaid for the specific account
        """
        try:
            
            options = AccountsBalanceGetRequestOptions(account_ids=[self.plaid_account_id])
            request = AccountsBalanceGetRequest(access_token=self.item.access_token, options=options)
            response = plaid_client.accounts_balance_get(request)
            accounts = response['accounts']
            if accounts:
                account = accounts[0]

                available_balance = account.get("balances").get("available")
                current_balance = account.get("balances").get("current")
                last_update = timezone.now()

                self.available_balance = available_balance
                self.current_balance = current_balance
                self.last_update = last_update
                self.save(update_fields=["available_balance", "current_balance", "last_update"])
                
                return (
                    {
                        "account_id": account.get("account_id"),
                        "available_balance": available_balance,
                        "current_balance": current_balance,
                        "name": account.get("name"),
                        "official_name": account.get("official_name"),
                        "type": str(account.get("type"))
                    },
                    last_update
                )
            else:
                return {}
   
        except PlaidApiException as e:
            self._handle_api_exception(exception=e, item=self.item)
            raise PlaidApiException(e)

    def get_transactions(self, start_date=None, end_date=None, offset=0):
        
        from purse_finance.models.plaid_transaction import PlaidTransaction
        
        all_transactions = []
        trans_objects = []
        try:
            while True:
                options = TransactionsGetRequestOptions(offset=offset, account_ids=[self.plaid_account_id])
                request = TransactionsGetRequest(
                        access_token=self.item.access_token,
                        start_date=start_date if start_date else self._calculate_start_date(),
                        end_date=self.today if not end_date else end_date,
                        options=options
                    )
                response = plaid_client.transactions_get(request)
                fetched_transactions = response['transactions']
                all_transactions.extend(fetched_transactions)
                
                trans_objects.extend(
                    [
                        PlaidTransaction(
                                amount=transaction.amount * -1,
                                is_income=True if transaction.amount * -1 > 0 else False,
                                transaction_id=transaction.transaction_id,
                                date=transaction.date,
                                name=transaction.name,
                                merchant_name=transaction.merchant_name,
                                is_pending=transaction.pending,
                                category_id=transaction.category_id,
                                plaid_account=self,
                        ) for transaction in fetched_transactions
                    ]
                )
                
                if len(fetched_transactions) < 100:
                    PlaidTransaction.objects.bulk_create(trans_objects, ignore_conflicts=True)
                    return self._serialize_transaction_data(all_transactions)
                else:
                    offset += 100

        except PlaidApiException as e:
            self._handle_api_exception(exception=e, item=self.item)
            raise PlaidApiException(e)