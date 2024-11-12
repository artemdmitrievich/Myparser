"""
Программа для автоматического получения сигналов по стратегии скальпинг на бирже yobit.net
"""

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


def ex_coin1():
    print("Некорректное значение coin1")


def ex_coin2():
    print("Некорректное значение coin2")


# Запуск автоматического отслеживания криптовалюты
def start_tracking_crypto(time_sleep, *args, **kwargs):

    My_Yobit = Yobit(*args, **kwargs)
    Is_valid_coins = My_Yobit.is_valid_coins()

    if Is_valid_coins == "Invalid coin1":
        ex_coin1()
        return

    elif Is_valid_coins == "Invalid coin2":
        ex_coin2()
        return

    # print(f"\n Началось отслеживание {My_Yobit.get_abbreviation_crypto}")
    list_avarage_trades_ask = []
    list_avarage_trades_bid = []
    while True:
        # print(list_avarage_trades_ask)
        # print(list_avarage_trades_bid)
        # print(Yobit().get_avarage_trades_ask())
        # print(Yobit().get_avarage_trades_bid())
        if len(list_avarage_trades_ask) == 0 and My_Yobit.get_avarage_trades_ask() != 0:
            number = My_Yobit.get_avarage_trades_ask()
            if number != 0:
                list_avarage_trades_ask.append(My_Yobit.get_avarage_trades_ask())
            # print(list_avarage_trades_ask)
            # print(list_avarage_trades_bid)
        elif len(list_avarage_trades_ask) == 4:
            try:
                if (
                    My_Yobit.get_avarage_trades_ask() != list_avarage_trades_ask[3]
                    and My_Yobit.get_avarage_trades_ask() != 0
                ):
                    number = My_Yobit.get_avarage_trades_ask()
                    if number != 0:
                        list_avarage_trades_ask.append(
                            My_Yobit.get_avarage_trades_ask()
                        )
                        list_avarage_trades_ask.pop(0)
                    # print("Сработал append")
                    # print(list_avarage_trades_ask)
                    # print(list_avarage_trades_bid)
            except:
                pass
        else:
            try:
                if (
                    My_Yobit.get_avarage_trades_ask()
                    != list_avarage_trades_ask[len(list_avarage_trades_ask) - 1]
                ) and My_Yobit.get_avarage_trades_ask() != 0:
                    number = My_Yobit.get_avarage_trades_ask()
                    if number != 0:
                        list_avarage_trades_ask.append(
                            My_Yobit.get_avarage_trades_ask()
                        )
                    # print("Сработал append")
                    # print(list_avarage_trades_ask)
                    # print(list_avarage_trades_bid)
            except:
                pass

        if (
            len(list_avarage_trades_ask) == 4
            and list_avarage_trades_ask[1] < list_avarage_trades_ask[0]
            and list_avarage_trades_ask[2] < list_avarage_trades_ask[1]
            and list_avarage_trades_ask[3] > list_avarage_trades_ask[2]
        ):
            Buy_signal(My_Yobit)

        if len(list_avarage_trades_bid) == 0 and My_Yobit.get_avarage_trades_bid() != 0:
            number = My_Yobit.get_avarage_trades_bid()
            if number != 0:
                list_avarage_trades_bid.append(My_Yobit.get_avarage_trades_bid())
            # print(list_avarage_trades_ask)
            # print(list_avarage_trades_bid)
        elif len(list_avarage_trades_bid) == 4:
            try:
                if (
                    My_Yobit.get_avarage_trades_bid()
                    != list_avarage_trades_bid[len(list_avarage_trades_bid) - 1]
                ) and My_Yobit.get_avarage_trades_bid() != 0:
                    number = My_Yobit.get_avarage_trades_bid()
                    if number != 0:
                        list_avarage_trades_bid.append(
                            My_Yobit.get_avarage_trades_bid()
                        )
                        list_avarage_trades_bid.pop(0)
                    # print("Сработал append")
                    # print(list_avarage_trades_ask)
                    # print(list_avarage_trades_bid)
            except:
                pass

        else:
            if (
                My_Yobit.get_avarage_trades_bid()
                != list_avarage_trades_bid[len(list_avarage_trades_bid) - 1]
            ) and My_Yobit.get_avarage_trades_bid() != 0:
                number = My_Yobit.get_avarage_trades_bid()
                if number != 0:
                    list_avarage_trades_bid.append(My_Yobit.get_avarage_trades_bid())
                # print("Сработал append")
                # print(list_avarage_trades_ask)
                # print(list_avarage_trades_bid)

        if (
            len(list_avarage_trades_bid) == 4
            and list_avarage_trades_bid[1] > list_avarage_trades_bid[0]
            and list_avarage_trades_bid[2] > list_avarage_trades_bid[1]
            and list_avarage_trades_bid[3] < list_avarage_trades_bid[2]
        ):
            Sell_signal(My_Yobit)

        # print(
        #     f"\nЦикл прошёл итерацию; len(list_avarage_trades_ask) = {len(list_avarage_trades_ask)};\nlen(list_avarage_trades_bid) = {len(list_avarage_trades_bid)}",
        #     end="",
        # )

        sleep(time_sleep)


if __name__ == "__main__":
    start_tracking_crypto(time_sleep=5)
