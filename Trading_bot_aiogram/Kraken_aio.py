import asyncio, krakenex, time, sqlite3
import pandas as pd
from Bot import send_message


class MovingAverageCrossover:

    def __init__(
        self, Id, pair_index, coin1, coin2, short_window, long_window, interval=1
    ):
        self.coin1 = coin1
        self.coin2 = coin2
        self.pair = coin1.upper() + coin2.upper()
        self.short_window = short_window
        self.long_window = long_window
        self.interval = interval  # Интервал в минутах
        self.api = krakenex.API()
        self.Id = Id
        self.pair_index = pair_index

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

    def __calculate_ema(self, prices, window):
        # return prices.rolling(window=window).mean()
        return prices.ewm(span=window, adjust=False).mean()

    def __check_signals(self):
        data = self.__fetch_data()
        if data == "error":
            return "error"
        prices = pd.DataFrame(data)  # Преобразуем данные в DataFrame
        prices = prices.iloc[:, 4]  # Закрывающие цены (5-й столбец)
        prices = prices.astype(float)

        # Вычисляем скользящие средние
        short_ema = self.__calculate_ema(prices, self.short_window)
        long_ema = self.__calculate_ema(prices, self.long_window)

        # Проверяем пересечения
        if (
            short_ema.iloc[-1] > long_ema.iloc[-1]
            and short_ema.iloc[-2] < long_ema.iloc[-2]
        ):
            self._Buy_Signal()
        elif (
            short_ema.iloc[-1] < long_ema.iloc[-1]
            and short_ema.iloc[-2] > long_ema.iloc[-2]
        ):
            self._Sell_Signal()
        else:
            self._Not_Signal()

    def _Buy_Signal(self):
        asyncio.get_event_loop().run_until_complete(
            send_message(self.Id, f"Сигнал на покупку {self.coin1} в {self.coin2}")
        )

    def _Sell_Signal(self):
        asyncio.get_event_loop().run_until_complete(
            send_message(self.Id, f"Сигнал на продажу {self.coin1} в {self.coin2}")
        )

    def _Not_Signal(self):
        asyncio.get_event_loop().run_until_complete(
            send_message(
                self.Id,
                f"Нет сигнала на покупку или\nпродажу {self.coin1} в {self.coin2}",
            )
        )

    def __check_stop_signals(self):
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (self.Id,))
        item = cursor.fetchone()

        if self.pair_index == item[1]:
            cursor.execute(
                """
                        UPDATE users_tracking SET stop_flag = ? WHERE Id = ?""",
                (
                    None,
                    self.Id,
                ),
            )
            conn.commit()
            return "break"

        elif item[1]:
            if self.pair_index in item[1]:
                cursor.execute(
                    """
                            UPDATE users_tracking SET stop_flag = ? WHERE Id = ?""",
                    (
                        item[1].replace(self.pair_index, ""),
                        self.Id,
                    ),
                )
                conn.commit()
                return "break"

        conn.close()

    def run(self):
        while True:
            if self.__check_stop_signals() == "break":
                break
            curr_check = self.__check_signals()
            if curr_check == "error":
                return
            if self.interval >= 1 and self.interval <= 60:
                time.sleep(60)
            else:
                time.sleep(300)


if __name__ == "__main__":
    MovingAverageCrossover("1270674543", "3_4;", "BTC", "USD", 20, 50, 1).run()
