import pytest

from purse_async.tasks import sync_plaid_accounts_task


@pytest.fixture(scope="function")
def mock_plaid_public_token_exchange(monkeypatch):

    def delay(user_id):
        return user_id
    
    monkeypatch.setattr(sync_plaid_accounts_task, "delay", delay)