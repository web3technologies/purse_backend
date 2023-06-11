import pytest

from django.contrib.auth import get_user_model
from django.utils import timezone

from purse_finance.models import CryptoAccount
from purse_finance.serializers.networth import NetWorth


@pytest.mark.django_db
class TestNetworthViewset:

    url = "/finance/networth/"

    def test_list_networths(self, 
        authenticated_api_client
    ):

        user = get_user_model().objects.get(id=1)
        networths = NetWorth.objects.filter(user=user)

        expected_res = [
                {"networth": networth.networth, "date": networth.date} 
                for networth 
                in networths
            ]

        response = authenticated_api_client.get(self.url)
        
        assert response.status_code == 200
        assert response.data == expected_res


@pytest.mark.django_db
class TestNetworthLive:

    url = "/finance/networth-live"

    def test_get_live_networth(self, 
        mocker,
        authenticated_api_client,
        item_and_plaid_account,
        ):

        _, plaid_account = item_and_plaid_account

        mocker.patch('purse_core.client.plaid_client.accounts_balance_get', return_value={'accounts': [
            {
                'account_id': plaid_account.plaid_account_id,
                'balances': {'available': 100.0, 'current': 200.0},
                'name': 'Test Account',
                'official_name': 'Test Official Account',
                'type': 'checking',
            }
        ]})
        crypto_account = CryptoAccount.objects.create(
            user_id=1,
            ticker="BTC",
            name="Bitcoin",
            amount=21,
            type="CRYPTO"
        )

        mocker.patch('purse_core.client.CoinMarketCapClient.make_request', return_value={
                    "id":1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "quote": {"USD": {"price": 100000}}
                })
        response = authenticated_api_client.get(self.url)

        assert response.status_code == 200
        assert response.data.get("networth") == 1071400.0
        assert response.data.get("date").strftime("%Y%m%d") == timezone.now().strftime("%Y%m%d")