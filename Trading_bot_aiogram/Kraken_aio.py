import asyncio, krakenex, time, sqlite3
import pandas as pd
from Bot import send_message


# Класс с инициализацией остлеживания криптовалюты
class MovingAverageCrossover:

    def __init__(
        self,
        Id=0,
        pair_index="3_4;",
        coin1="BTC",
        coin2="USD",
        short_window=20,
        long_window=50,
        interval=1,
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

    # Получение текущей стоимости криптовалюты на kraken.com
    def current_coin1_price(self):
        response = self.api.query_public("Ticker", {"pair": self.coin1 + "USD"})
        return float(response["result"][list(response["result"].keys())[0]]["c"][0])

    def __ex_coins(self):
        print("Ошибка ввода данных")
        asyncio.get_event_loop().run_until_complete(
            send_message(
                self.Id,
                f"Произошла ошибка ввода данных '__ex_coins', прошу напишите об этом владельцу бота.",
            )
        )

    # Получение информации по валютной паре с kraken.com
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

    # Вычисление экспоненциалной скользящей средней
    def __calculate_ema(self, prices, window):
        # return prices.rolling(window=window).mean()
        return prices.ewm(span=window, adjust=False).mean()

    # Проверка наличия возможности для покупки или продажи
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
            # self._Sell_Signal()
        elif (
            short_ema.iloc[-1] < long_ema.iloc[-1]
            and short_ema.iloc[-2] > long_ema.iloc[-2]
        ):
            self._Sell_Signal()
            # self._Buy_Signal()

        # elif self.Id == 1270674543:
        #     self._Not_Signal()
        #     self._Buy_Signal()
        #     self._Sell_Signal()

    # Обработчик сигнала на покупку
    def _Buy_Signal(self):
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT current_sum, is_auto_operation, operation_percent FROM users_demo_account WHERE Id = ?",
            (self.Id,),
        )
        item = cursor.fetchone()

        if item:
            operation_amount = item[0] * item[2] // 100
            if operation_amount >= 1 and item[1] == "True":
                conn_currency = sqlite3.connect("users_currency_base.db")
                cursor_currency = conn_currency.cursor()
                cursor_currency.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {"user" + str(self.Id)} (
                        currency_name TEXT PRIMARY KEY,
                        currency_quantity REAL,
                        last_signal TEXT
                    )
                """
                )

                cursor_currency.execute(
                    f"SELECT currency_quantity, last_signal FROM {'user' + str(self.Id)} WHERE currency_name = ?",
                    (self.coin1,),
                )
                item_currency = cursor_currency.fetchone()
                if item_currency:
                    if item_currency[1] != "Buy":
                        cursor.execute(
                            "UPDATE users_demo_account SET current_sum = ? WHERE Id = ?",
                            (
                                item[0] - operation_amount,
                                self.Id,
                            ),
                        )
                        conn.commit()
                        conn.close()
                        cursor_currency.execute(
                            f"""
                            UPDATE {"user" + str(self.Id)} SET currency_quantity = ?,
                            last_signal = ?
                            WHERE currency_name = ?
                        """,
                            (
                                item_currency[0]
                                + operation_amount / self.current_coin1_price(),
                                "Buy",
                                self.coin1,
                            ),
                        )
                else:
                    cursor.execute(
                        "UPDATE users_demo_account SET current_sum = ? WHERE Id = ?",
                        (
                            item[0] - operation_amount,
                            self.Id,
                        ),
                    )
                    conn.commit()
                    conn.close()
                    cursor_currency.execute(
                        f"INSERT INTO {'user' + str(self.Id)} ("
                        f"currency_name,"
                        f"currency_quantity,"
                        f"last_signal"
                        f") VALUES (?, ?, ?)",
                        (
                            self.coin1,
                            operation_amount / self.current_coin1_price(),
                            "Buy",
                        ),
                    )

                conn_currency.commit()
                conn_currency.close()
        else:
            conn.close()

        # Отправка сообщения с сигналом ботом
        asyncio.get_event_loop().run_until_complete(
            send_message(self.Id, f"Сигнал на покупку {self.coin1} в {self.coin2}")
        )

    # Обработчик сигнала на продажу
    def _Sell_Signal(self):
        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        table_name = "user" + str(self.Id)
        cursor_currency.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        result = cursor_currency.fetchone()
        if result:
            cursor_currency.execute(
                f"SELECT currency_quantity, last_signal FROM {table_name} WHERE currency_name = ?",
                (self.coin1,),
            )
            currency = cursor_currency.fetchone()
            if currency:
                if currency[1] != "Sell":
                    currency_quantity = currency[0]
                    cursor_currency.execute(
                        f"DELETE FROM {table_name} WHERE currency_name = ?",
                        (self.coin1,),
                    )
                    conn_currency.commit()

                    conn = sqlite3.connect("Data_base.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT current_sum FROM users_demo_account WHERE Id = ?",
                        (self.Id,),
                    )
                    current_sum = cursor.fetchone()[0]
                    cursor.execute(
                        f"UPDATE users_demo_account SET current_sum = ? WHERE Id = ?",
                        (
                            current_sum
                            + float(self.current_coin1_price() * currency_quantity),
                            self.Id,
                        ),
                    )
                    conn.commit()
                    conn.close()
        conn_currency.close()

        # Отправка сообщения с сигналом ботом
        asyncio.get_event_loop().run_until_complete(
            send_message(self.Id, f"Сигнал на продажу {self.coin1} в {self.coin2}")
        )

    # Обработчик отсутствия сигнала (Не нужен в итоговой версии)
    def _Not_Signal(self):
        asyncio.get_event_loop().run_until_complete(
            send_message(
                self.Id,
                f"Нет сигнала на покупку или\nпродажу {self.coin1} в {self.coin2}",
            )
        )

    # Проверка наличия сигнала
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

    # Запуск отслеживания
    def run(self):
        while True:
            # Проверка на наличие стоп сигнала
            if self.__check_stop_signals() == "break":
                return

            # Проверка сигнала на покупку или продажу
            curr_check = self.__check_signals()

            # Проверка на наличие ошибки
            if curr_check == "error":
                return

            # Пауза
            if self.interval >= 1 and self.interval <= 60:
                time.sleep(60)
            else:
                time.sleep(300)


if __name__ == "__main__":
    print(
        MovingAverageCrossover(
            "1270674543", "3_4;", "BTC", "USD", 20, 50, 1
        ).current_coin1_price()
    )
