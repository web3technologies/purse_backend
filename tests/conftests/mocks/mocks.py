import pytest

from django.conf import settings

import plaid
from plaid.api import plaid_api
from plaid.model import item_public_token_exchange_request, item_get_request, accounts_balance_get_request 

from purse_core import client

@pytest.fixture(scope="function")
def mock_plaid_api_client(monkeypatch):
    
    class MockApiClient:
        def __init__(self, configuration):
            self.configuration = configuration

    monkeypatch.setattr(plaid, "ApiClient", MockApiClient)


@pytest.fixture(scope="function")
def mock_plaid_api(monkeypatch):
    class MockPlaidApi:
        
        def __init__(self, *args):
            self.args = args
        
        def item_public_token_exchange(self, exchange_request):
            return {"access_token": "mock_access_token"}

        def item_get(self, request):
            return {
                "item": {"error": None}
            }

        def accounts_balance_get(self, request):
            
            return {
                "accounts": [               
                    {
                        "account_id": "1234",
                        "balances": {"available": 100, "current": 100},
                        "name": "test",
                        "official_name": "test",
                        "type": "checkings"
                    },
                    {
                        "account_id": "1235",
                        "balances": {"available": 200, "current": 200},
                        "name": "test",
                        "official_name": "test",
                        "type": "checkings"
                    },
                    {
                        "account_id": "1236",
                        "balances": {"available": 300, "current": 300},
                        "name": "test",
                        "official_name": "test",
                        "type": "checkings"
                    }
                ]
            }

    monkeypatch.setattr(client, "plaid_client", MockPlaidApi)


@pytest.fixture(scope="function")
def mock_plaid_public_token_exchange(monkeypatch):

    class MockItemPublicTokenExchangeRequest:
        def __init__(self, public_token="") -> None:
            ...
    
    monkeypatch.setattr(item_public_token_exchange_request, "ItemPublicTokenExchangeRequest", MockItemPublicTokenExchangeRequest)


@pytest.fixture(scope="function")
def mock_item_get_request(monkeypatch):

    class MockItemGetRequest:
        def __init__(self, public_token="") -> None:
            ...
    
    monkeypatch.setattr(item_get_request, "ItemGetRequest", MockItemGetRequest)

