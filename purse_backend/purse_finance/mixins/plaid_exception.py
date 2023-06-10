import datetime
import json

from django.conf import settings
from django.utils import timezone

from purse_catalog.models import PlaidApiError


class PlaidUtilityMixin:


    """
        This class contains some utility methods for processing the data returned by the Plaid Client Library

    """

    def __init__(self) -> None:
        self.today = timezone.now().today().date()


    def _handle_api_exception(self, exception, item):
        """
            When there is an api exception raised this method is used to handle the exception and update the item and accounts linked 
        """

        exception_message = json.loads(exception.body)
        error_code = exception_message.get("error_code")
        plaid_error = PlaidApiError.objects.get(error_code=error_code)
        if plaid_error.is_login_required:
            status = settings.LOGIN_REQUIRED
        else:
            status = settings.INTENAL_ERROR
        item.status = status
        item.plaid_internal_status = plaid_error
        item.save(update_fields=["status", "plaid_internal_status"])
        item.plaidaccount_set.all().update(status=status)


    def _calculate_start_date(self):
        year_to_use = self.today.year
        
        if self.today.month < 4: 
            if self.today.month == 1:
                year_to_use = self.today.year - 1
                month_3_months_ago = 11
            elif self.today.month == 2:
                year_to_use = self.today.year - 1
                month_3_months_ago = 12
            elif self.today.month == 3:
                year_to_use = self.today.year
                month_3_months_ago = 1
        else:
            month_3_months_ago = self.today.month - 3

        start_date = datetime.datetime.strptime(f"{year_to_use}-{month_3_months_ago}-01", '%Y-%m-%d').date()

        return start_date

    def _serialize_transaction_data(self, transactions):
        """
        This should probably be a serializer
        """
        from purse_finance.models import PlaidAccount

        if transactions:
            transaction_data = []

            for transaction in transactions:
                try:
                    plaid_account = PlaidAccount.objects.get(plaid_account_id=transaction.account_id)
                    account_name = plaid_account.name
                except PlaidAccount.DoesNotExist:
                    account_name = "unknown"
                transaction_data.append(
                    {
                        "transaction_id": transaction.transaction_id,
                        "account_id": transaction.account_id,
                        "account_name": account_name,     # this is not optimal but will leave for now
                        "account_type": plaid_account.account_type,
                        "amount": transaction.amount * -1,     # add negative because income from plaid is negative so reverse the number for display
                        "category": transaction.category,
                        "date": transaction.date,
                        "merchant_name": transaction.merchant_name,
                        "name": transaction.name,
                        "personal_finance_category": transaction.personal_finance_category
                    }
                )

            return transaction_data
        else:
            return []

