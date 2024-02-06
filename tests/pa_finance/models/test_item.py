
from datetime import date
import pytest

from django.conf import settings

from plaid.exceptions import ApiException as PlaidApiException

from purse_catalog.models import PlaidApiError


@pytest.mark.django_db
class TestItemModel:

    def test_str_method(self, item_and_plaid_account):
        item, _ = item_and_plaid_account
        assert str(item) == f"{item.institution} -- {item.status}"

    def test_get_account_data(self, mocker, item_and_plaid_account):

        item, plaid_account = item_and_plaid_account

        mocker.patch('purse_core.client.plaid_client.accounts_balance_get', return_value={'accounts': [
            {
                'account_id': plaid_account.plaid_account_id,
                'balances': {'available': 100.0, 'current': 200.0},
                'name': 'Test Account',
                'official_name': 'Test Official Account',
                'type': 'checking',
            }
        ]})

        account_data = item.get_account_data()

        assert account_data == [
            {
                'account_id': plaid_account.plaid_account_id,
                'available_balance': 100.0,
                'current_balance': 200.0,
                'name': 'Test Account',
                'official_name': 'Test Official Account',
                'type': 'checking',
            }
        ]
        plaid_account.refresh_from_db()
        assert plaid_account.available_balance == 100
        assert plaid_account.current_balance == 200

    def test_get_account_data_api_exception(
            self, 
            mocker, 
            item_and_plaid_account, 
            mock_plaid_accounts_balance_get_api_exception
    ):
        
        item, _ = item_and_plaid_account
        with pytest.raises(PlaidApiException):
            item.get_account_data()

        item.refresh_from_db()
        assert item.plaid_internal_status == PlaidApiError.objects.get(error_code="ITEM_LOGIN_REQUIRED")
        assert item.status == settings.LOGIN_REQUIRED
        assert all(
            [plaid_account.status == settings.LOGIN_REQUIRED for plaid_account in item.plaidaccount_set.all()]
        )

    def test_get_transactions(self, mocker, mock_plaid_transaction_obj):

        item, plaid_account, plaid_transaction_object = mock_plaid_transaction_obj

        mocker.patch('purse_core.client.plaid_client.transactions_get', return_value={'transactions': [plaid_transaction_object]})

        transactions = item.get_transactions()

        assert transactions == [
            {
                'transaction_id': 'G5nPkyG6yXU7WrgBgMyzU98Zn7z3lxUG4aGex', 
                'account_id': plaid_account.plaid_account_id, 
                'account_name': '', 
                'account_type': '', 
                'amount': -25.0, 
                'category': ['Payment', 'Credit Card'], 
                'date': date(2023, 3, 31), 
                'merchant_name': "test", 
                'name': 'CREDIT CARD 3333 PAYMENT *//', 
                'personal_finance_category': None
            }
        ]

    def test_get_transactions_with_dates(self, mocker, item_and_plaid_account):

        item, _ = item_and_plaid_account

        mocker.patch('purse_core.client.plaid_client.transactions_get', return_value={'transactions': []})

        start_date = date(2022, 1, 1)
        end_date = date(2022, 1, 31)
        transactions = item.get_transactions(start_date=start_date, end_date=end_date)

        assert transactions == []


    def test_get_transactions_api_exception(
            self, 
            item_and_plaid_account, 
            mock_plaid_accounts_transaction_get_api_exception
    ):
        
        item, _ = item_and_plaid_account
        with pytest.raises(PlaidApiException):
            item.get_transactions()

        item.refresh_from_db()
        assert item.plaid_internal_status == PlaidApiError.objects.get(error_code="ITEM_LOGIN_REQUIRED")
        assert item.status == settings.LOGIN_REQUIRED
        assert all(
            [plaid_account.status == settings.LOGIN_REQUIRED for plaid_account in item.plaidaccount_set.all()]
        )
        
