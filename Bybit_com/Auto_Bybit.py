from Bybit_parser import Bybit
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
def start_tracking_crypto(
    coin1="btc", coin2="usd", time_sleep=18, support=0, resistance=999999999
):
    My_Bybit = Bybit(coin1=coin1, coin2=coin2)
    stack_ask = []
    stack_bid = []

    while True:
        try:
            My_Bybit.get_average_trades_ask()
            sleep(2)
            My_Bybit.get_average_trades_bid()
            sleep(2)
            if len(stack_ask) == 0:
                stack_ask.append(
                    (My_Bybit.get_average_trades_ask(), My_Bybit.get_avarage_spread())
                )
                sleep(2)

            elif len(stack_ask) == 4:
                stack_ask.append(
                    (My_Bybit.get_average_trades_ask(), My_Bybit.get_avarage_spread())
                )
                stack_ask.pop(0)
                sleep(2)

            else:
                curr_ask = My_Bybit.get_average_trades_ask()
                if curr_ask != stack_ask[len(stack_ask) - 1][0]:
                    stack_ask.append((curr_ask, My_Bybit.get_avarage_spread()))
                sleep(2)

            if len(stack_bid) == 0:
                stack_bid.append(
                    (My_Bybit.get_average_trades_bid(), My_Bybit.get_avarage_spread())
                )
                sleep(2)

            elif len(stack_bid) == 4:
                stack_bid.append(
                    (My_Bybit.get_average_trades_bid(), My_Bybit.get_avarage_spread())
                )
                stack_bid.pop(0)
                sleep(2)

            else:
                curr_bid = My_Bybit.get_average_trades_bid()
                if curr_bid != stack_bid[len(stack_bid) - 1][0]:
                    stack_bid.append((curr_bid, My_Bybit.get_avarage_spread()))
                sleep(2)
        except:
            pass

        if (
            len(stack_bid) == 4
            and stack_bid[1][0] < stack_bid[0][0]
            and stack_bid[2][0] < stack_bid[1][0]
            and stack_bid[3][0] > stack_bid[2][0]
            and stack_bid[1][1] <= stack_bid[0][1]
            and stack_bid[2][1] <= stack_bid[1][1]
            and stack_bid[1][0] > support
            and stack_bid[3][0] > support
            and stack_bid[2][0] < support
        ):
            Buy_signal(My_Bybit)

        elif (
            len(stack_ask) == 4
            and stack_ask[1][0] > stack_ask[0][0]
            and stack_ask[2][0] > stack_ask[1][0]
            and stack_ask[3][0] < stack_ask[2][0]
            and stack_ask[1][1] <= stack_ask[0][1]
            and stack_ask[2][1] <= stack_ask[1][1]
            and stack_ask[1][0] < resistance
            and stack_ask[3][0] < resistance
            and stack_ask[2][0] > resistance
        ):
            Sell_signal(My_Bybit)

        sleep(time_sleep - 16)


# start_tracking_crypto()
