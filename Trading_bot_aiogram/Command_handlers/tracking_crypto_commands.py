import sqlite3, krakenex
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Keyboards.inline_buttons import create_delete_keyboard
from Bot import bot


tracking_crypto_commands_router = Router()


class Form_start_tracking(StatesGroup):
    waiting_for_message_start_tracking = State()


@tracking_crypto_commands_router.message(Command("adding_crypto"))
async def adding_crypto(message: types.Message, state: FSMContext):
    await state.set_state(Form_start_tracking.waiting_for_message_start_tracking)
    await message.answer(
        text="""Чтобы добавить криптовалютную пару в отслеживание,
введи данные в формате:
Валюта1,
Валюта2,
параметр короткой скользящей средней,
параметр длинной скользящей средней,
длительность свечи в минутах.
В качестве разделителя используй запятую!"""
    )


@tracking_crypto_commands_router.message(
    Form_start_tracking.waiting_for_message_start_tracking
)
async def process_message_start_tracking(message: types.Message, state: FSMContext):
    # Пробуем разбиваем текст на список
    try:
        text = str(message.text).split(",")
        sucsess = True
    except:
        await message.answer("Неверный формат ввода данных!")
        sucsess = False

    # Проверяем его длину
    if sucsess and len(text) != 5:
        await message.answer("Неверный формат ввода данных!")
        sucsess = False

    # Проверяем значение интервала
    if sucsess:
        interval = text[4].replace(" ", "")
        if interval in ["1m", "5m", "15m", "30m", "1h", "1d", "1w"]:
            dictionary = {
                "1m": 1,
                "5m": 5,
                "15m": 15,
                "30m": 30,
                "1h": 60,
                "1d": 1440,
                "1w": 10080,
            }
            interval = dictionary[interval]
        else:
            sucsess = False
            await message.answer(
                "Некорректно указана длительность свечи,\nдоступные варианты свечей:\n'1m', '5m', '15m', '30m', '1h', '1d', '1w'"
            )

    # Проверяем значения криптовалют
    if sucsess:
        try:
            coin1 = text[0].strip().upper()
            coin2 = text[1].strip().upper()
            if krakenex.API().query_public(
                "OHLC", {"pair": f"{coin1}{coin2}", "interval": interval}
            )["error"]:
                await message.answer("Введены некорректные значения валют!")
                sucsess = False
        except:
            await message.answer("Введены некорректные значения валют!")
            sucsess = False

    # Проверяем значение скользящих средних
    if sucsess:
        try:
            short_window = int(text[2].strip())
            long_window = int(text[3].strip())
            if not (
                short_window < long_window
                and 2 <= short_window <= 100
                and 15 <= long_window <= 200
            ):
                await message.answer(
                    """Скользящие средние должны принимать
целочисленные значения, короткая
средняя от 2 до 100, длинная от 15
до 200, при этом значение длинной
должно быть больше, чем значение
короткой"""
                )
                sucsess = False
        except:
            await message.answer(
                """Скользящие средние должны принимать
целочисленные значения, короткая
средняя от 5 до 100, длинная от 50
до 200, при этом значение длинной
должно быть больше, чем значение
короткой"""
            )
            sucsess = False

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tracking_quantity FROM users_tracking")
    items = cursor.fetchall()
    cursor.execute(
        "SELECT stop_flag, tracking_quantity FROM users_tracking WHERE Id = ?",
        (message.from_user.id,),
    )
    item = cursor.fetchone()
    if item[0]:
        user_stop_flag = item[0]
    else:
        user_stop_flag = ""
    conn.close()

    # Определяем количество всех криптовалют, находящихся в отслеживании у всех пользователей
    sum_items = 0
    for i in items:
        sum_items += i[0]

    quantity_employed_slots = item[1] + user_stop_flag.count(";")

    if sucsess:
        if item[1] < 3:
            if sum_items < 15:
                if quantity_employed_slots < 3:
                    conn = sqlite3.connect("Data_base.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT * FROM users_tracking WHERE Id = ?",
                        (message.from_user.id,),
                    )
                    item = cursor.fetchone()

                    tracking_quantity = item[2] + 1

                    if item[1]:
                        item_1 = item[1]
                    else:
                        item_1 = ""

                    if item[8] == "False" and "3_4;" not in item_1:
                        cursor.execute(
                            """
                            UPDATE users_tracking SET tracking_quantity = ?,coin1_first = ?,
                            coin2_first = ?, short_window_first = ?, long_window_first = ?,
                            interval_first = ?, is_tracking_first = ? WHERE Id = ?""",
                            (
                                tracking_quantity,
                                coin1,
                                coin2,
                                short_window,
                                long_window,
                                interval,
                                "Waiting",
                                message.from_user.id,
                            ),
                        )

                    elif item[14] == "False" and "9_10;" not in item_1:
                        cursor.execute(
                            """
                            UPDATE users_tracking SET tracking_quantity = ?, coin1_second = ?,
                            coin2_second = ?, short_window_second = ?, long_window_second = ?,
                            interval_second = ?, is_tracking_second = ? WHERE Id = ?""",
                            (
                                tracking_quantity,
                                coin1,
                                coin2,
                                short_window,
                                long_window,
                                interval,
                                "Waiting",
                                message.from_user.id,
                            ),
                        )

                    elif item[20] == "False" and "15_16;" not in item_1:
                        cursor.execute(
                            """
                            UPDATE users_tracking SET tracking_quantity = ?, coin1_third = ?,
                            coin2_third = ?, short_window_third = ?, long_window_third = ?,
                            interval_third = ?, is_tracking_third = ? WHERE Id = ?""",
                            (
                                tracking_quantity,
                                coin1,
                                coin2,
                                short_window,
                                long_window,
                                interval,
                                "Waiting",
                                message.from_user.id,
                            ),
                        )

                    conn.commit()
                    conn.close()

                    await message.answer(
                        f"Криптовалютная пара {coin1} в {coin2}\nуспешно добавлена в отслеживание!"
                    )
                else:
                    await message.answer(
                        "Извините, нет свободных слотов на отслеживание криптовалюты!\nПовторите попытку через 1 и через 5 минут."
                    )
            else:
                await message.answer(
                    "Нет свободных мест на отслеживание,\nлимит на всех пользователей: 15\nповторите попытку позже"
                )
        else:
            await message.answer("Слишком много криптовалют\nбыло добавлено\nлимит: 3")

    await state.clear()


@tracking_crypto_commands_router.message(Command("profile"))
async def profile(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()
    message_text = (
        "Профиль:\n\nКриптовалют отслеживается:\n" + str(item[2]) + " из 3.\n\n"
    )

    dictionary = {
        1: "1m",
        5: "5m",
        15: "15m",
        30: "30m",
        60: "1h",
        1440: "1d",
        10080: "1w",
    }

    if item[2] != 0:
        if item[2] == 3:
            interval_first = dictionary[item[7]]
            interval_second = dictionary[item[13]]
            interval_third = dictionary[item[19]]
            message_text += f"1) {item[3]} в {item[4]},\nпараметр короткой скользящей средней = {item[5]},\nпараметр длинной скользящей средней = {item[6]},\nдлительность свечи = {interval_first};\n\n"
            message_text += f"2) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи = {interval_second};\n\n"
            message_text += f"3) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи = {interval_third};\n\n"

        elif item[2] == 1:
            if item[8] != "False":
                interval_first = dictionary[item[7]]
                message_text += f"1) {item[3]} в {item[4]},\nпараметр короткой скользящей средней = {item[5]},\nпараметр длинной скользящей средней = {item[6]},\nдлительность свечи = {interval_first};\n\n"
            elif item[14] != "False":
                interval_second = dictionary[item[13]]
                message_text += f"1) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи = {interval_second};\n\n"
            else:
                interval_third = dictionary[item[19]]
                message_text += f"1) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи = {interval_third};\n\n"

        else:
            if item[8] == "False":
                interval_second = dictionary[item[13]]
                interval_third = dictionary[item[19]]
                message_text += f"1) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи = {interval_second};\n\n"
                message_text += f"2) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи = {interval_third};\n\n"
            else:
                interval_first = dictionary[item[7]]
                message_text += f"1) {item[3]} в {item[4]},\nпараметр короткой скользящей средней = {item[5]},\nпараметр длинной скользящей средней = {item[6]},\nдлительность свечи = {interval_first};\n\n"
                if item[14] == "False":
                    interval_third = dictionary[item[19]]
                    message_text += f"2) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи = {interval_third};\n\n"
                else:
                    interval_second = dictionary[item[13]]
                    message_text += f"2) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи = {interval_second};\n\n"

    else:
        message_text += "У вас не отслеживается ни одной криптовалюты\nдля начала отслеживания,\nиспользуйте команду '/adding_crypto'"
    await message.answer(message_text)


@tracking_crypto_commands_router.message(Command("stop"))
async def stop(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()

    if item[2] != 0:
        await message.answer(
            "Выберите криптовалюту, которую вы\nбольше не хотите отслеживать:",
            reply_markup=create_delete_keyboard(message.from_user.id),
        )
    else:
        await message.answer(
            f"{message.from_user.first_name}, у вас не отслеживается ни одной криптовалюты\nдля начала отслеживания,\nиспользуйте команду '/adding_crypto'"
        )


@tracking_crypto_commands_router.callback_query(
    lambda c: c.data in ["delete_all", "delete_first", "delete_second", "delete_third"]
)
async def on_delete_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users_tracking WHERE Id = ?", (callback_query.from_user.id,)
    )
    item = cursor.fetchone()

    if item[1]:
        curr_stop_flag = item[1]
    else:
        curr_stop_flag = ""

    if item[2] != 0:
        if callback_query.data == "delete_all":
            index_delete_all = ""
            if item[3] and item[8] != "Waiting":
                index_delete_all += "3_4;"
            if item[9] and item[14] != "Waiting":
                index_delete_all += "9_10;"
            if item[15] and item[20] != "Waiting":
                index_delete_all += "15_16;"

            if index_delete_all == "":
                index_delete_all = None

            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?,
                    coin1_first = ?, coin2_first = ?, short_window_first = ?, long_window_first = ?, interval_first = ?, is_tracking_first = ?,
                    coin1_second = ?, coin2_second = ?, short_window_second = ?, long_window_second = ?, interval_second = ?, is_tracking_second = ?,
                    coin1_third = ?, coin2_third = ?, short_window_third = ?, long_window_third = ?, interval_third = ?, is_tracking_third = ?
                    WHERE Id = ?
                    """,
                (
                    index_delete_all,
                    0,
                    None,
                    None,
                    0,
                    0,
                    0,
                    "False",
                    None,
                    None,
                    0,
                    0,
                    0,
                    "False",
                    None,
                    None,
                    0,
                    0,
                    0,
                    "False",
                    callback_query.from_user.id,
                ),
            )
            conn.commit()

            await callback_query.message.answer(
                "Все криптовалюты успешно\nудалены из отслеживания!"
            )

        elif callback_query.data == "delete_first":
            if item[8] != "Waiting":
                stop_flag = curr_stop_flag + "3_4;"
            else:
                if curr_stop_flag != "":
                    stop_flag = curr_stop_flag
                else:
                    stop_flag = None

            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?, coin1_first = ?,
                    coin2_first = ?, short_window_first = ?, long_window_first = ?,
                    interval_first = ?, is_tracking_first = ? WHERE Id = ?""",
                (
                    stop_flag,
                    item[2] - 1,
                    None,
                    None,
                    0,
                    0,
                    0,
                    "False",
                    callback_query.from_user.id,
                ),
            )
            conn.commit()

            await callback_query.message.answer(
                f"Пара {item[3]}_{item[4]} успешно\nудалена из отслеживания!"
            )

        elif callback_query.data == "delete_second":
            if item[14] != "Waiting":
                stop_flag = curr_stop_flag + "9_10;"
            else:
                if curr_stop_flag != "":
                    stop_flag = curr_stop_flag
                else:
                    stop_flag = None

            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?, coin1_second = ?,
                    coin2_second = ?, short_window_second = ?, long_window_second = ?,
                    interval_second = ?, is_tracking_second = ? WHERE Id = ?""",
                (
                    stop_flag,
                    item[2] - 1,
                    None,
                    None,
                    0,
                    0,
                    0,
                    "False",
                    callback_query.from_user.id,
                ),
            )
            conn.commit()

            await callback_query.message.answer(
                f"Пара {item[9]}_{item[10]} успешно\nудалена из отслеживания!"
            )

        else:
            if item[14] != "Waiting":
                stop_flag = curr_stop_flag + "15_16;"
            else:
                if curr_stop_flag != "":
                    stop_flag = curr_stop_flag
                else:
                    stop_flag = None

            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?, coin1_third = ?,
                    coin2_third = ?, short_window_third = ?, long_window_third = ?,
                    interval_third = ?, is_tracking_third = ? WHERE Id = ?""",
                (
                    stop_flag,
                    item[2] - 1,
                    None,
                    None,
                    0,
                    0,
                    0,
                    "False",
                    callback_query.from_user.id,
                ),
            )
            conn.commit()

            await callback_query.message.answer(
                f"Пара {item[15]}_{item[16]} успешно\nудалена из отслеживания!"
            )

    conn.close()
