import asyncio, time, sqlite3
# from Bot import bot
from aiogram import Dispatcher, types
from user_private import user_private_router
from common.bot_cmds_list import private
# from file import Func
from multiprocessing import Process

import krakenex
import pandas as pd
from Signals_messages import Sell_signal_message, Buy_signal_message

import os
from aiogram import Bot
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))

async def send_message(Id, message_text):
    await bot.send_message(chat_id=Id, text=message_text)

def Func():
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users"
    )
    item = cursor.fetchone()
    if item:
        if item[2] == 1:
            Id = item[0]
            conn.close()
            curr = MovingAverageCrossover(item[0], item[3], item[4], item[5], item[6], item[7])
            curr_f = curr.run
            process = Process(target=curr_f)
            process.start()
            # asyncio.get_event_loop().run_until_complete(send_message(Id, "Туц"))
    else:
        conn.close()


ALLOWED_UPDATES = ['message, edit_message']

dp = Dispatcher()

dp.include_router(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    process = Process(target=Func)
    process.start()
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
if __name__ == "__main__":
    asyncio.run(main())


class MovingAverageCrossover:

    def __init__(self, Id, coin1, coin2, short_window, long_window, interval=1):
        self.coin1 = coin1
        self.coin2 = coin2
        self.pair = coin1.upper() + coin2.upper()
        self.short_window = short_window
        self.long_window = long_window
        self.interval = interval  # Интервал в минутах
        self.api = krakenex.API()
        self.Id = Id

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
            self._Buy_Signal()

    def _Buy_Signal(self):
        # print(f"Сигнал на покупку {self.coin1} в {self.coin2}")
        asyncio.get_event_loop().run_until_complete(send_message(self.Id, f"Сигнал на покупку {self.coin1} в {self.coin2}"))

    def _Sell_Signal(self):
        # print(f"Сигнал на продажу {self.coin1} в {self.coin2}")
        asyncio.get_event_loop().run_until_complete(send_message(self.Id, f"Сигнал на продажу {self.coin1} в {self.coin2}"))
    
    # def _Not_Signal(self):
    #     asyncio.get_event_loop().run_until_complete(send_message(self.Id, "Нет сигнала на продажу или покупку"))

    def run(self):
        while True:
            curr_check = self.__check_signals()
            if curr_check == "error":
                return
            time.sleep(
                self.interval * 10
            )  # задержка между запросами длительностью в одну свечу
