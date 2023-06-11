from django.utils.functional import SimpleLazyObject

from coinbase.wallet.error import NotFoundError
from requests.exceptions import HTTPError

from purse_core.client import (
    AlphaVantageClient, 
    coinbase_client, 
    CoinMarketCapClient, 
    CoinGeckoClient
)


class CryptoService:

    _equity_percent = .51
    
    _av_client = AlphaVantageClient()
    _cb_client = coinbase_client
    _cg_client = CoinGeckoClient()
    _cmc_client = CoinMarketCapClient()


    def get_account_value(self, ticker, amount):

        # first attempt to fetch price data from coinbase
        try:
            price = self._cb_client.get_spot_price(currency_pair=f"{ticker}-USD").amount
        except NotFoundError as e:      # Coinbase does not support some currencies
            try:
                price = self._cmc_client.get_price(ticker)
            except HTTPError as e:
                try:
                    price = self._cg_client.get_price(ticker)
                except HTTPError as e:
                    try:
                        price = self._av_client.get_price(ticker)
                    except HTTPError as e:
                        raise e

        return float(price) * float(amount) * self._equity_percent
    
crypto_service = SimpleLazyObject(CryptoService)