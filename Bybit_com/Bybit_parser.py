from Bybit_keys import api, secret
from pybit.unified_trading import HTTP

""" 
ask больше bid
ask - цена, по которой я могу купить, по которой другие продают
bid - цена, по которой я могу продать, по которой другие покупают
"""


session = HTTP(testnet=True)


class Bybit:

    def __init__(self, coin1="BTC", coin2="USDT"):
        self.__coin1 = coin1.upper()
        self.__coin2 = coin2.upper()
        self._bid = None
        self._ask = None

    # Получение инкапсулированных свойств
    @property
    def get_abbreviation_crypto(self):
        return self.__coin1

    def get_average_trades_bid(self):
        bids = session.get_orderbook(
            category="linear", symbol=self.__coin1.upper() + self.__coin2.upper()
        )["result"]["b"]
        sum_bid = 0
        quntitity_bid = 0
        for bid in bids:
            sum_bid += float(bid[0]) * float(bid[1])
            quntitity_bid += float(bid[1])
        self._bid = sum_bid / quntitity_bid
        return sum_bid / quntitity_bid

    def get_average_trades_ask(self):
        asks = session.get_orderbook(
            category="linear", symbol=self.__coin1.upper() + self.__coin2.upper()
        )["result"]["a"]
        sum_ask = 0
        quntitity_ask = 0
        for ask in asks:
            sum_ask += float(ask[0]) * float(ask[1])
            quntitity_ask += float(ask[1])
        self._ask = sum_ask / quntitity_ask
        return sum_ask / quntitity_ask

    def get_avarage_spread(self):
        return self._ask - self._bid


# print(Bybit().get_avarage_trades_bid())
# print(Bybit().get_avarage_trades_ask())
