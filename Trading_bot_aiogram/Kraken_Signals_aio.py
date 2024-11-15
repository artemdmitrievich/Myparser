import krakenex, time
import pandas as pd
from Signals_messages import Sell_signal_message, Buy_signal_message


class MovingAverageCrossover:

    def __init__(self, query, coin1, coin2, short_window, long_window, interval=1):
        self.coin1 = coin1
        self.coin2 = coin2
        self.pair = coin1.upper() + coin2.upper()
        self.short_window = short_window
        self.long_window = long_window
        self.interval = interval  # Интервал в минутах
        self.api = krakenex.API()
        self.query = query

    def __ex_coins(self):
        print("Ошибка ввода данных")

    def __fetch_data(self):
        response = self.api.query_public(
            "OHLC", {"pair": self.pair, "interval": self.interval}
        )
        if response["error"]:
            self.__ex_coins()
            return "error"
            # raise Exception(f"Error fetching data: {response['error']}")
        else:
            return response["result"][list(response["result"].keys())[0]]

    def __calculate_sma(self, prices, window):
        return prices.rolling(window=window).mean()

    def __check_signals(self):
        data = self.__fetch_data()
        if data == "error":
            return "error"
        prices = pd.DataFrame(data)  # Преобразуем данные в DataFrame
        prices = prices.iloc[:, 4]  # Закрывающие цены (5-й столбец)
        prices = prices.astype(float)

        # Вычисляем скользящие средние
        short_sma = self.__calculate_sma(prices, self.short_window)
        long_sma = self.__calculate_sma(prices, self.long_window)

        # Проверяем пересечения
        if (
            short_sma.iloc[-1] > long_sma.iloc[-1]
            and short_sma.iloc[-2] < long_sma.iloc[-2]
        ):
            self._Buy_Signal()
        elif (
            short_sma.iloc[-1] < long_sma.iloc[-1]
            and short_sma.iloc[-2] > long_sma.iloc[-2]
        ):
            self._Sell_Signal()
        
        else:
            self._Sell_Signal()

    def _Buy_Signal(self):
        # print(f"Сигнал на покупку {self.coin1} в {self.coin2}")
        Buy_signal_message(query=self.query)

    def _Sell_Signal(self):
        # print(f"Сигнал на продажу {self.coin1} в {self.coin2}")
        Sell_signal_message(query=self.query)

    def run(self):
        while True:
            curr_check = self.__check_signals()
            if curr_check == "error":
                return
            time.sleep(
                self.interval * 10
            )  # задержка между запросами длительностью в одну свечу


# Пример использования
if __name__ == "__main__":
    ma_crossover = MovingAverageCrossover(
        coin1="sol", coin2="usd", short_window=20, long_window=50
    )
    ma_crossover.run()
