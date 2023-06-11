import datetime
import pytest



@pytest.mark.django_db
class TestPlaidViewset:

    url = "/finance/transactions"

    def test_list_transactions(self, mocker,
        authenticated_api_client,
        mock_plaid_transaction_obj):

        _, plaid_account, plaid_transaction_object = mock_plaid_transaction_obj

        mocker.patch('purse_core.client.plaid_client.transactions_get', return_value={'transactions': [plaid_transaction_object]})

        response = authenticated_api_client.get(self.url)
        
        assert response.status_code == 200
        assert response.data == [
            {
                'transaction_id': 'G5nPkyG6yXU7WrgBgMyzU98Zn7z3lxUG4aGex', 
                'account_id': plaid_account.plaid_account_id, 
                'account_name': '', 
                'account_type': '', 
                'amount': -25.0, 
                'category': ['Payment', 'Credit Card'], 
                'date': datetime.date(2023, 3, 31), 
                'merchant_name': "test", 
                'name': 'CREDIT CARD 3333 PAYMENT *//', 
                'personal_finance_category': None
            },
            {
                'transaction_id': 'G5nPkyG6yXU7WrgBgMyzU98Zn7z3lxUG4aGex', 
                'account_id': plaid_account.plaid_account_id, 
                'account_name': '', 
                'account_type': '', 
                'amount': -25.0, 
                'category': ['Payment', 'Credit Card'], 
                'date': datetime.date(2023, 3, 31), 
                'merchant_name': "test", 
                'name': 'CREDIT CARD 3333 PAYMENT *//', 
                'personal_finance_category': None
            }
        ]
