import requests
import json

from django.conf import settings


class CoinMarketCapClient:

    _api_key = settings.COINMARKETCAP_API_KEY
    _base_api_url = settings.COINMARKETCAP_URL

    def get_price(self, ticker):

        parameters = {
                'convert':'USD',
                "symbol": ticker
            }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self._api_key,
        }
        response = requests.get(
            f"{self._base_api_url}/v1/cryptocurrency/quotes/latest",
            params=parameters,
            headers=headers
        )
        response.raise_for_status()
        json_res = json.loads(response.text).get("data")
        price = json_res.get(ticker).get("quote").get("USD").get("price")
        return price

