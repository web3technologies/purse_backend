import json
import requests


class CoinGeckoClient:

    base_url = "https://api.coingecko.com/api/v3"

    def get_coin_id(self, ticker):
        """
            Coin Gecko has strage lookup
            Must find the coin id by iterating through list
        """

        response = requests.get(f"{self.base_url}/coins/list")
        response.raise_for_status()
        coin_list = json.loads(response.text)
        for coin in coin_list:
            if ticker.lower() == coin["symbol"]:
                return coin['id']

    def get_price(self, ticker):
        coin_id = self.get_coin_id(ticker)
        response = requests.get(f"{self.base_url}/coins/{coin_id}")
        response.raise_for_status()
        price = json.loads(response.text).get("market_data").get("current_price").get('usd')
        return price