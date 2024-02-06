import datetime
import json
import pytest


from django.conf import settings
from django.utils import timezone
from plaid.exceptions import ApiException as PlaidApiException

from purse_catalog.models import PlaidApiError


@pytest.mark.django_db
class TestPlaidAccount:

    def test_get_account_data_by_account(self, mocker, item_and_plaid_account):
        _, plaid_account = item_and_plaid_account

        mocker.patch('purse_core.client.plaid_client.accounts_balance_get', return_value={
            'accounts': [
                {
                    'account_id': '123',
                    'balances': {
                        'available': 100.0,
                        'current': 150.0
                    },
                    'name': 'Checking',
                    'official_name': 'Checking Account',
                    'type': 'checking'
                }
            ]
        })

        plaid_account.get_account_data_by_account()
        plaid_account.refresh_from_db()

        assert plaid_account.available_balance == 100.0
        assert plaid_account.current_balance == 150.0
        assert plaid_account.last_update.date() == timezone.now().date()

    def test_get_account_data_by_account_api_exception(
            self, 
            mock_plaid_accounts_balance_get_api_exception, 
            item_and_plaid_account
        ):
        item, plaid_account = item_and_plaid_account

        with pytest.raises(PlaidApiException):
            plaid_account.get_account_data_by_account()

        item.refresh_from_db()

        assert item.plaid_internal_status == PlaidApiError.objects.get(error_code="ITEM_LOGIN_REQUIRED")
        assert item.status == settings.LOGIN_REQUIRED
        assert all(
            [plaid_account.status == settings.LOGIN_REQUIRED for plaid_account in item.plaidaccount_set.all()]
        )

    def test_get_transactions(self, mocker, mock_plaid_transaction_obj):

        _, plaid_account, plaid_transaction_object = mock_plaid_transaction_obj

        mocker.patch(
            'purse_core.client.plaid_client.transactions_get', 
            return_value={'transactions': [plaid_transaction_object]}
        )

        transactions = plaid_account.get_transactions()

        assert len(transactions) == 1
        assert transactions[0]['transaction_id'] == 'G5nPkyG6yXU7WrgBgMyzU98Zn7z3lxUG4aGex'
        assert transactions[0]["account_id"] == plaid_account.plaid_account_id
        assert transactions[0]["account_name"] == plaid_account.name
        assert transactions[0]["account_type"] == plaid_account.account_type
        assert transactions[0]['amount'] == -25.0
        assert transactions[0]['category'] == ['Payment', 'Credit Card']
        assert transactions[0]['date'] == datetime.date(2023, 3, 31)
        assert transactions[0]['merchant_name'] == 'test'
        assert transactions[0]['name'] == 'CREDIT CARD 3333 PAYMENT *//'
        assert transactions[0]['personal_finance_category'] == None


    def test_get_transactions_api_exception(
            self, 
            item_and_plaid_account, 
            mock_plaid_accounts_transaction_get_api_exception
    ):

        item, plaid_account = item_and_plaid_account

        with pytest.raises(PlaidApiException):
            plaid_account.get_transactions()

        item.refresh_from_db()
        assert item.plaid_internal_status == PlaidApiError.objects.get(error_code="ITEM_LOGIN_REQUIRED")
        assert item.status == settings.LOGIN_REQUIRED
        assert all(
            [plaid_account.status == settings.LOGIN_REQUIRED for plaid_account in item.plaidaccount_set.all()]
        )
