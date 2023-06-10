import json
import pytest


from django.conf import settings
from django.contrib.auth import get_user_model

from purse_finance.serializers.item import ItemSerializer, Item
from purse_finance.models import PlaidAccount


@pytest.mark.django_db
class TestItemViewset:

    url = "/finance/item/"

    def test_list_items(self, 
        authenticated_api_client,
        mock_plaid_item_get
    ):

        user = get_user_model().objects.get(id=1)
        items = Item.objects.filter(user=user)

        response = authenticated_api_client.get(self.url)
        
        assert response.status_code == 200
        assert response.data == ItemSerializer(items, many=True).data


    def test_retrieve_item(self,
            authenticated_api_client,
        ):

        item = Item.objects.get(id=1)

        url = f"{self.url}{item.id}/"

        response = authenticated_api_client.get(url)
        assert response.status_code == 200
        # assert response.data == ItemSerializerDetail(item).data

    def test_list_items_bad_item(self, 
        authenticated_api_client,
        mock_plaid_api_bad_item
    ):

        user = get_user_model().objects.get(id=1)
        items = Item.objects.filter(user=user)

        response = authenticated_api_client.get(self.url)
        
        items_after = items.all()

        assert response.status_code == 200
        assert response.data == ItemSerializer(items, many=True).data
        assert all(
            [item.status == settings.LOGIN_REQUIRED for item in items_after]
        )
        

    def test_create_item(
        self, 
        authenticated_api_client,
        mock_plaid_item_public_token_exchange
    ):
        """
            Test to make sure that the item is created and that the accounts linked are well created.
        """
    
        
        items_before = Item.objects.count()
        plaid_accounts_before = PlaidAccount.objects.count()

        data = {
            "public_token": 'test',
            "accounts": [
                {
                    "type": "DEPOSITORY",
                    "id": "test",
                    "name": "PLAIDTEST1", 
                },
                {
                    "type": "INVESTMENT",
                    "id": "test1",
                    "name": "PLAIDTEST2",
                },
                {
                    "type": "INVESTMENT",
                    "id": "test2",
                    "name": "PLAIDTEST3",
                }
            ]
        }

        response = authenticated_api_client.post(self.url, data=data, format="json")
        items_after = Item.objects.count()
        plaid_accounts_after = PlaidAccount.objects.count()

        assert response.status_code == 201
        assert items_after == items_before + 1
        assert plaid_accounts_after == plaid_accounts_before + len(data["accounts"])
        assert response.data["access_token"] == "mock_access_token" and response.data["status"] == "ACTIVE"


    def test_create_item_duplicate_plaid_account_id(
        self, 
        authenticated_api_client,
        mock_plaid_item_public_token_exchange
    ):
        """
            Test to make sure that if the same account by account id is passed that the unique constraint does not create a new account and there is no exception raised
        """
        
        items_before = Item.objects.count()
        plaid_accounts_before = PlaidAccount.objects.count()

        data = {
            "public_token": 'test',
            "accounts": [
                {
                    "type": "DEPOSITORY",
                    "id": "test",
                    "name": "PLAIDTEST", 
                },
                {
                    "type": "DEPOSITORY",
                    "id": "test",
                    "name": "PLAIDTEST", 
                }
            ]
        }

        response = authenticated_api_client.post(self.url, data=data, format="json")
        items_after = Item.objects.count()
        plaid_accounts_after = PlaidAccount.objects.count()

        assert response.status_code == 201
        assert items_after == items_before + 1
        assert plaid_accounts_after == plaid_accounts_before + 1
        assert response.data["access_token"] == "mock_access_token" and response.data["status"] == "ACTIVE"


    def test_patch_item(
        self, 
        authenticated_api_client,
        mock_plaid_public_token_exchange
    ):
        
        item = Item.objects.filter(user_id=1, status="ACTIVE").last()
        item.status = settings.LOGIN_REQUIRED
        item.save(update_fields=["status"])

        data = {
            "status": "ACTIVE",
            "item_id": item.id
        }

        response = authenticated_api_client.patch(self.url, data=data, format="json")
        
        item.refresh_from_db()

        assert response.status_code == 200
        assert item.status == "ACTIVE"