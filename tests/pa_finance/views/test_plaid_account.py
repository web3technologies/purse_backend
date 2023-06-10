import pytest

from django.contrib.auth import get_user_model
from purse_finance.serializers.account import PlaidAccountSerializer
from purse_finance.models import PlaidAccount


@pytest.mark.django_db
class TestPlaidViewset:

    url = "/finance/accounts/"

    def test_list_plaid_accounts(self, 
        authenticated_api_client
    ):

        user = get_user_model().objects.get(id=1)
        plaid_accounts = PlaidAccount.objects.filter(user=user)

        response = authenticated_api_client.get(self.url)
        
        assert response.status_code == 200
        assert response.data == PlaidAccountSerializer(plaid_accounts, many=True).data


    def test_get_plaid_account_pass_bad_id(self, 
        authenticated_api_client
    ):

        """
            Test the id of the account passed does not exist
        """

        response = authenticated_api_client.get(f"{self.url}3/")

        assert response.status_code == 404