from datetime import timedelta
import pytest

from django.utils import timezone

from purse_finance.models import Item, PlaidAccount, CryptoAccount
from purse_catalog.models import PlaidApiError


@pytest.fixture(scope="function")
def item_and_plaid_account(user):

    item = Item.objects.create(
        access_token='access_token',
        date_created=timezone.now(),
        date_updated=timezone.now(),
        status='ACTIVE',
        plaid_internal_status=PlaidApiError(id=1),
        plaid_item_id='plaid_item_id',
        institution='institution',
        user=user,
    )

    plaid_account = PlaidAccount.objects.create(
            plaid_account_id="zysbsdlcbnw2ds614a",
            item=item,
            available_balance = 25,
            current_balance = 40,
            last_update = timezone.now() - timedelta(days=1),
            user=user
    )
    
    return item, plaid_account


@pytest.fixture(scope="function")
def crypto_account(user):

    crypto_account = CryptoAccount.objects.create(
        user=user,
        ticker="BTC",
        name="Bitcoin",
        amount=21,
        type="CRYPTO"
    )
    
    return crypto_account