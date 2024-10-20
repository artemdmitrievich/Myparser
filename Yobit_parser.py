import requests


# Класс криптобиржи Yobit.com
class Yobit:

    def __init__(self, crypto="btc", currency="usd", limit=150):
        self.__crypto = crypto
        self.__currency = currency
        self.__limit = limit

    # Получение инкапсулированных свойств
    @property
    def get_abbreviation_crypto(self):
        return self.__crypto

    # Получение всей информации с Yobit Api
    def get_info():
        response = requests.get(url="https://yobit.net/api/3/info")
        return response.text

    # Получение всех валютных пар с Yobit Api
    def get_tecker(self):
        response = requests.get(
            url=f"https://yobit.net/api/3/ticker/{self.__crypto}_{self.__currency}?ignore_invalid=1"
        )
        with open("ticker.txt", "w") as file:
            file.write(response.text)
        return response.text

    # Получение общей стоимости продажи когкретной криптовалюты с Yobit Api
    def get_depth(self):
        response = requests.get(
            url=f"https://yobit.net/api/3/depth/{self.__crypto}_{self.__currency}?limit={self.__limit}&ignore_invalid=1"
        )
        bids = response.json()[f"{self.__crypto}_{self.__currency}"]["bids"]
        total_bids_amount = 0
        for item in bids:
            price = item[0]
            coin_amount = item[1]
            total_bids_amount += price * coin_amount
        return total_bids_amount

    # Получение общей стоимости покупки когкретной криптовалюты с Yobit Api
    def get_total_trades_ask(self):
        response = requests.get(
            url=f"https://yobit.net/api/3/trades/{self.__crypto}_{self.__currency}?limit={self.__limit}&ignore_invalid=1"
        )
        total_trade_ask = 0
        for item in response.json()[f"{self.__crypto}_{self.__currency}"]:
            if item["type"] == "ask":
                total_trade_ask += item["price"] * item["amount"]
        return total_trade_ask

    # Получение общей стоимости покупки когкретной криптовалюты с Yobit Api
    def get_total_trades_bid(self):
        response = requests.get(
            url=f"https://yobit.net/api/3/trades/{self.__crypto}_{self.__currency}?limit={self.__limit}&ignore_invalid=1"
        )
        total_trade_bid = 0
        for item in response.json()[f"{self.__crypto}_{self.__currency}"]:
            if item["type"] == "bid":
                total_trade_bid += item["price"] * item["amount"]
        return total_trade_bid

    # Получение средней стоимости продажи когкретной криптовалюты с Yobit Api
    def get_average_trades_ask(self):
        response = requests.get(
            url=f"https://yobit.net/api/3/trades/{self.__crypto}_{self.__currency}?limit={self.__limit}&ignore_invalid=1"
        )
        total_price_ask = 0
        total_amount_ask = 0
        for item in response.json()[f"{self.__crypto}_{self.__currency}"]:
            if item["type"] == "ask":
                total_price_ask += item["price"] * item["amount"]
                total_amount_ask += item["amount"]
        average_trade_ask = total_price_ask / total_amount_ask
        return average_trade_ask

    # Получение средней стоимости прокупки когкретной криптовалюты с Yobit Api
    def get_average_trades_bid(self):
        response = requests.get(
            url=f"https://yobit.net/api/3/trades/{self.__crypto}_{self.__currency}?limit={self.__limit}&ignore_invalid=1"
        )
        total_price_bid = 0
        total_amount_bid = 0
        for item in response.json()[f"{self.__crypto}_{self.__currency}"]:
            if item["type"] == "bid":
                total_price_bid += item["price"] * item["amount"]
                total_amount_bid += item["amount"]
        average_trade_bid = total_price_bid / total_amount_bid
        return average_trade_bid
