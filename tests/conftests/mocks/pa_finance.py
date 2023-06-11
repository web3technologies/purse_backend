from django.conf import settings

from datetime import date
import json
import pytest

from plaid.exceptions import ApiException as PlaidApiException
from plaid.model.location import Location
from plaid.model.payment_meta import PaymentMeta
from plaid.model.transaction import Transaction


@pytest.fixture(scope="function")
def mock_plaid_transaction_obj(item_and_plaid_account):

    item, plaid_account = item_and_plaid_account

    transaction_obj_data = {
            'account_id': plaid_account.plaid_account_id,
            'account_owner': None,
            'amount': 25.0,
            'authorized_date': date(2023, 3, 30),
            'authorized_datetime': None,
            'category': ['Payment', 'Credit Card'],
            'category_id': '16001000',
            'check_number': None,
            'date': date(2023, 3, 31),
            'datetime': None,
            'iso_currency_code': 'USD',
            'location': Location(**{'address': None,
                        'city': None,
                        'country': None,
                        'lat': None,
                        'lon': None,
                        'postal_code': None,
                        'region': None,
                        'store_number': None}),
            'merchant_name': "test",
            'name': 'CREDIT CARD 3333 PAYMENT *//',
            'payment_channel': 'other',
            'payment_meta': PaymentMeta(**{'by_order_of': None,
                            'payee': None,
                            'payer': None,
                            'payment_method': None,
                            'payment_processor': None,
                            'ppd_id': None,
                            'reason': None,
                            'reference_number': None}),
            'pending': False,
            'pending_transaction_id': None,
            'personal_finance_category': None,
            'transaction_code': None,
            'transaction_id': 'G5nPkyG6yXU7WrgBgMyzU98Zn7z3lxUG4aGex',
            'transaction_type': 'special',
            'unofficial_currency_code': None
        }

    plaid_transaction_object = Transaction(**transaction_obj_data)

    return item, plaid_account, plaid_transaction_object


@pytest.fixture(scope="function")
def mock_plaid_accounts_balance_get_api_exception(mocker):

    class MockHttpResp:
        status = 400
        reason = "test"
        data = json.dumps({"error_code": "ITEM_LOGIN_REQUIRED"})
        def getheaders():
            return None

    mocker.patch(
        'purse_core.client.plaid_client.accounts_balance_get',
        side_effect=PlaidApiException(
            reason="test",
            status="test",
            http_resp=MockHttpResp
        )
    )


@pytest.fixture(scope="function")
def mock_plaid_accounts_transaction_get_api_exception(mocker):

    class MockHttpResp:
        status = 400
        reason = "test"
        data = json.dumps({"error_code": "ITEM_LOGIN_REQUIRED"})
        def getheaders():
            return None

    mocker.patch(
        'purse_core.client.plaid_client.transactions_get',
        side_effect=PlaidApiException(
            reason="test",
            status="test",
            http_resp=MockHttpResp
        )
    )



@pytest.fixture(scope="function")
def mock_plaid_item_get(mocker):
    mocker.patch(
        'purse_core.client.plaid_client.item_get',
        return_value={"item": {"error": None}}
    )


@pytest.fixture(scope="function")
def mock_plaid_api_bad_item(mocker):
        
    mocker.patch(
        'purse_core.client.plaid_client.item_get',
        return_value={
        "item": {
            "error": {
                "error_code": settings.LOGIN_REQUIRED
                }
            }
        }
    )


@pytest.fixture(scope="function")
def mock_plaid_item_public_token_exchange(mocker):
        
    mocker.patch(
        'purse_core.client.plaid_client.item_public_token_exchange',
        return_value={"access_token": "mock_access_token"}
    )