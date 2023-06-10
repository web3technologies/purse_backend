import datetime
import json
import pytest
from requests.exceptions import HTTPError

from django.conf import settings
from django.utils import timezone



@pytest.mark.django_db
class TestCryptoAccount:

    def test_get_value_from_coinmarketcap(self, mocker, crypto_account):

        _price = 100000

        mocker.patch('purse_core.client.CoinMarketCapClient.make_request', return_value={
                    "id":1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "quote": {"USD": {"price": _price}}
                })
        

        value = crypto_account.get_value()
        
        assert value == crypto_account.amount * _price * .51

    def test_get_value_from_alphavantage(self, mocker, crypto_account):

        _price = 28092.64000000

        mocker.patch('purse_core.client.CoinMarketCapClient.make_request', side_effect=HTTPError())

        mocker.patch('purse_core.client.AlphaVantageClient.make_request', 
                return_value={
                    'Realtime Currency Exchange Rate': 
                    {
                    '1. From_Currency Code': 'BTC', 
                      '2. From_Currency Name': 'Bitcoin', 
                      '3. To_Currency Code': 'USD', 
                      '4. To_Currency Name': 'United States Dollar', 
                      '5. Exchange Rate': _price, 
                      '6. Last Refreshed': '2023-04-03 00:43:01', 
                      '7. Time Zone': 'UTC', 
                      '8. Bid Price': '28092.63000000', 
                      '9. Ask Price': '28092.64000000'
                      }
                }
        )
        

        value = crypto_account.get_value()
        
        assert value == crypto_account.amount * _price * .51




