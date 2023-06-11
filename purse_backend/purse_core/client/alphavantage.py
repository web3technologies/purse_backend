import requests

from django.conf import settings



class AlphaVantageClient:

    url = f"{settings.ALPHAVANTAGE_URL}/query"

    def get_price(self, ticker):

        querystring = {
            "function": "CURRENCY_EXCHANGE_RATE", 
            "from_currency": ticker.upper(), 
            "to_currency": "USD",
            "apikey": settings.ALPHAVANTAGE_API_KEY
            }
        response = requests.request("GET", self.url, params=querystring)
        price = response.json()["Realtime Currency Exchange Rate"].get("5. Exchange Rate")
        return price