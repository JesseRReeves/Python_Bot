from models.order import OrderResponse
from utils.load_env import *
from binance.client import Client




class Binance:
    def __init__(self):
        self.client = Client(binance_api_key, binance_api_secret)
    

    
    def buy(
            self, coin: str, amount_in_vs_currency: float, vs_currency: str ="USDT"
    ) -> OrderResponse:
        response = self.client.order_market_buy(
            symbol=(coin + vs_currency).upper(),
        quoteOrderQty=amount_in_vs_currency,
        )
        return OrderResponse.from_dict(response)
    

    def sell(self, coin: str, amount_in_vs_currency: float) -> OrderResponse:
        response = self.client.order_market_sell(
            symbol=(coin).upper(),
            quoteOrderQty=amount_in_vs_currency,
        )
        return OrderResponse.from_dict(response)
    

    def get_current_price(self, coin: str) -> float:
        return float(self.client.get_ticker(symbol=coin)["lastPrice"])
    

# One thing to note is we’re using the python-binance library to interact with the Binance API.
#  This saves us from having to write our own wrapper. 

#   Another thing to bear in mind is the vs_currency parameter on the buy and sell methods.
#  We’ve named it the same as CoinGecko’s own parameter for consistency, however this refers to 
# the base asset that the exchange itself supports, not CoinGecko. For instance, most of 
# Binance’s pairs are in USDT but this is not a value that CoinGecko’s API returns.

#   Finally, the reason behind having a method that fetches the current price for a coin, is to
#  help us manage our exit strategy. We’ll use it in order to calculate the current stop loss 
# and take profit for assets the bot is holding.