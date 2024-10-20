from Yobit_parser import Yobit
from time import sleep


# Сигнал на покупку криптовалюты
def Buy_signal(copy):
    print("Сигнал на покупку")
    print(
        f" Цена перестала уменьшаться, вероятно, она начнёт расти.\n Советую купить {copy.get_abbreviation_crypto}"
    )


# Сигнал на продажу криптовалюты
def Sell_signal(copy):
    print("Сигнал на продажу")
    print(
        f" Цена перестала расти, вероятно, она начнёт уменьшаться.\n Советую продать имеющиеся {copy.get_abbreviation_crypto}"
    )


# Запуск автоматического отслеживания криптовалюты
def start_tracking_crypto(crypto="btc", currency="usd", limit=150, time_sleep=10):
    My_Yobit = Yobit(crypto="btc", currency="usd", limit=150)
    print(f"\n Началось отслеживание {My_Yobit.get_abbreviation_crypto}")
    list_average_trades_ask = []
    list_average_trades_bid = []
    while True:
        if len(list_average_trades_ask) == 0:
            list_average_trades_ask.append(My_Yobit.get_average_trades_ask())
        elif len(list_average_trades_ask) == 4:
            if My_Yobit.get_average_trades_ask() != list_average_trades_ask[3]:
                list_average_trades_ask.pop(0)
                list_average_trades_ask.append(My_Yobit.get_average_trades_ask())
                print("Сработал append")
        else:
            if (
                My_Yobit.get_average_trades_ask()
                != list_average_trades_ask[len(list_average_trades_ask) - 1]
            ):
                list_average_trades_ask.append(My_Yobit.get_average_trades_ask())
                print("Сработал append")

        if (
            len(list_average_trades_ask) == 4
            and list_average_trades_ask[1] < list_average_trades_ask[0]
            and list_average_trades_ask[2] < list_average_trades_ask[1]
            and list_average_trades_ask[3] > list_average_trades_ask[2]
        ):
            Buy_signal(My_Yobit)

        if len(list_average_trades_bid) == 0:
            list_average_trades_bid.append(My_Yobit.get_average_trades_ask())
        elif len(list_average_trades_bid) == 4:
            if (
                My_Yobit.get_average_trades_ask()
                != list_average_trades_bid[len(list_average_trades_bid) - 1]
            ):
                list_average_trades_bid.pop(0)
                list_average_trades_bid.append(My_Yobit.get_average_trades_ask())
                print("Сработал append")
        else:
            if (
                My_Yobit.get_average_trades_ask()
                != list_average_trades_bid[len(list_average_trades_bid) - 1]
            ):
                list_average_trades_bid.append(My_Yobit.get_average_trades_ask())
                print("Сработал append")

        if (
            len(list_average_trades_bid) == 4
            and list_average_trades_bid[1] > list_average_trades_bid[0]
            and list_average_trades_bid[2] > list_average_trades_bid[1]
            and list_average_trades_bid[3] < list_average_trades_bid[2]
        ):
            Sell_signal(My_Yobit)

        # print(
        #     f"\nЦикл прошёл итерацию; len(list_average_trades_ask) = {len(list_average_trades_ask)};\nlen(list_average_trades_bid) = {len(list_average_trades_bid)}",
        #     end="",
        # )

        sleep(time_sleep)
