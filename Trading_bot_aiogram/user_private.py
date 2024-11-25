import sqlite3, krakenex
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Keyboards.inline_buttons import (
    MyCallback,
    create_keyboard,
    create_delete_keyboard,
    create_is_auto_operation_keyboard,
    create_is_close_demo_account_keyboard,
    create_demo_account_transaction_keyboard,
    create_update_demo_account_keyboard,
)
from Parsers_aio.Main_info_crypto_parser import General
from Parsers_aio.Item_info_crypto_parser import Crypto
from on_start_update_data_base import on_start_update_data_base


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await on_start_update_data_base()

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()

    if not item:
        await message.reply(
            f"Привет, {message.from_user.first_name}, я твой виртуальный крипто помощник.",
            reply_markup=create_keyboard(),
        )
        cursor.execute(
            """
            INSERT OR IGNORE INTO users_tracking (
            Id, stop_flag, tracking_quantity,
            coin1_first, coin2_first, short_window_first, long_window_first, interval_first, is_tracking_first,
            coin1_second, coin2_second, short_window_second, long_window_second, interval_second, is_tracking_second,
            coin1_third, coin2_third, short_window_third, long_window_third, interval_third, is_tracking_third
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                message.from_user.id,
                None,
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
            ),
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO users_demo_account (
            Id, is_demo_account, start_sum, current_sum,
            is_auto_operation, operation_percent
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                message.from_user.id,
                "False",
                0,
                0,
                "False",
                0,
            ),
        )

    else:
        if item[2] != 0:
            index_delete_all = ""
            if item[3]:
                index_delete_all += "3_4;"
            if item[9]:
                index_delete_all += "9_10;"
            if item[15]:
                index_delete_all += "15_16;"

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
                    message.from_user.id,
                ),
            )

        cursor.execute(
            """
            UPDATE users_demo_account SET is_demo_account = ?, start_sum = ?,
            current_sum = ?, is_auto_operation = ?, operation_percent = ? WHERE Id = ?""",
            (
                "False",
                0,
                0,
                "False",
                0,
                message.from_user.id,
            ),
        )

        await message.reply(
            "Перезапуск прошёл успешно!\nВсе криптовалюты удалены из отслеживания",
            reply_markup=create_keyboard(),
        )

    conn.commit()
    conn.close()

    conn_currency = sqlite3.connect("users_currency_base.db")
    cursor_currency = conn_currency.cursor()
    cursor_currency.execute(
        f"DROP TABLE IF EXISTS {'user' + str(message.from_user.id)}"
    )
    conn_currency.commit()
    conn_currency.close()


@user_private_router.callback_query(MyCallback.filter(F.foo == "start_tracking"))
async def my_callback_foo(query: CallbackQuery):

    await query.message.answer(
        text="Для начала отслеживания введи команду '/adding_crypto'"
    )


class Form_start_tracking(StatesGroup):
    waiting_for_message_start_tracking = State()


@user_private_router.message(Command("adding_crypto"))
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


@user_private_router.message(Form_start_tracking.waiting_for_message_start_tracking)
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
                and 5 <= short_window <= 100
                and 50 <= long_window <= 200
            ):
                await message.answer(
                    """Скользящие средние должны принимать
целочисленные значения, короткая
средняя от 5 до 100, длинная от 50
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
        "SELECT stop_flag FROM users_tracking WHERE Id = ?", (message.from_user.id,)
    )
    user_stop_flag = cursor.fetchone()[0]
    conn.close()

    # Определяем количество всех криптовалют, находящихся в отслеживании
    sum_items = 0
    for i in items:
        sum_items += i[0]

    if user_stop_flag != "3_4;9_10;15_16;":
        if sum_items < 15:
            if sucsess:
                conn = sqlite3.connect("Data_base.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users_tracking WHERE Id = ?", (message.from_user.id,)
                )
                item = cursor.fetchone()

                if item[2] > 2:
                    limit = False
                else:
                    limit = True
                    tracking_quantity = item[2] + 1

                if item[1]:
                    item_1 = item[1]
                else:
                    item_1 = ""

                if item[8] == "False" and limit and "3_4;" not in item_1:
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

                elif item[14] == "False" and limit and "9_10;" not in item_1:
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

                elif item[20] == "False" and limit and "15_16;" not in item_1:
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
                elif item[2] == 3:
                    await message.answer(
                        "Слишком много криптовалют\nбыло добавлено\nлимит: 3"
                    )

                conn.commit()
                conn.close()
                if limit:
                    await message.answer(
                        f"Криптовалютная пара {coin1} в {coin2}\nуспешно добавлена в отслеживание!"
                    )
        else:
            await message.answer(
                "Нет свободных мест на отслеживание,\nлимит на всех пользователей: 15\nповторите попытку позже"
            )
    else:
        await message.answer(
            "Прошло слишком мало времени с завершения\nотслеживания последних 3 криптовалют!\nповторите попытку позже"
        )

    await state.clear()


@user_private_router.message(Command("profile"))
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


@user_private_router.message(Command("about"))
async def about(message: types.Message):
    await message.answer("Информация о боте:")


@user_private_router.message(Command("command_list"))
async def about(message: types.Message):
    await message.answer(
        """
Список доступных команд:

1. '/start' - Запуск | Перезапуск;
2. '/about' - Информация о боте;
3. '/profile' - Профиль;
4. '/command_list' - Полный список всех команд;
5. '/adding_crypto' - Добавить криптовалюту в отслеживание;
6. '/stop' - Прекратить отслеживание криптовалюты;
7. '/help' - Техподдержка.
8. '/get_total_capitalization' - Получить общую рыночную
капитализацию;
9. '/get_total_trading_volume' - Получить общий объём торгов;
10. '/get_crypto_capitalization' - Получить рыночную
капитализацию конкретной криптовалюты;
11. '/get_crypto_price' - Получить текущую среднюю
стоимость конкретной криптовалюты;
12. '/demo_account' - Демо-счёт для торговли;"""
    )


@user_private_router.message(Command("get_total_capitalization"))
async def get_total_capitalization(message: types.Message):
    curr_General = General()
    curr_capitalization = curr_General.get_data_market_capitalization()[0]
    curr_change = curr_General.get_change_market_capitalization()
    curr_change_value = curr_change[0]
    curr_direction = "увеличилась" if curr_change[2] == "up" else "уменьшилась"
    await message.answer(
        f"Общая рыночная каптилизация составляет:\n$ {curr_capitalization}\n\nРыночная капитализация {curr_direction}\nна {curr_change_value} за последние 24 часа."
    )


@user_private_router.message(Command("get_total_trading_volume"))
async def get_total_trading_volume(message: types.Message):
    curr_General = General()
    curr_volume = curr_General.get_total_trading_volume_per_day()[0]
    await message.answer(
        f"Общий объём торгов криптовалютой составляет:\n$ {curr_volume}"
    )


class Form_crypto_cap(StatesGroup):
    waiting_for_message_crypto_cap = State()


@user_private_router.message(Command("get_crypto_capitalization"))
async def get_crypto_capitalization(message: types.Message, state: FSMContext):
    await state.set_state(Form_crypto_cap.waiting_for_message_crypto_cap)
    await message.answer(
        "Для получения рыночной капитализации,\nвведите название криптовалюты:"
    )


@user_private_router.message(Form_crypto_cap.waiting_for_message_crypto_cap)
async def process_message_crypto_cap(message: types.Message, state: FSMContext):
    try:
        curr_Crypto = Crypto(message.text)
        curr_name = curr_Crypto.get_crypto_name
        curr_capitalization = curr_Crypto.get_current_crypto_capitalization()[0]
        if curr_capitalization != "Нет информации":
            await message.answer(
                f"Рыночная капитализация {curr_name}:\n$ {curr_capitalization}"
            )
        else:
            await message.answer(f"Нет информации о рыночной капитализации {curr_name}")
    except:
        await message.answer("Введена некорректная криптовалюта")

    await state.clear()


class Form_crypto_price(StatesGroup):
    waiting_for_message_crypto_price = State()


@user_private_router.message(Command("get_crypto_price"))
async def get_crypto_price(message: types.Message, state: FSMContext):
    await state.set_state(Form_crypto_price.waiting_for_message_crypto_price)
    await message.answer(
        "Для получения средней стоимости,\nвведите название криптовалюты:"
    )


@user_private_router.message(Form_crypto_price.waiting_for_message_crypto_price)
async def process_message_crypto_price(message: types.Message, state: FSMContext):
    try:
        curr_Crypto = Crypto(message.text)
        curr_name = curr_Crypto.get_crypto_name
        curr_price = curr_Crypto.get_current_average_crypto_price()[0]
        await message.answer(f"Средняя стоимость {curr_name}:\n$ {curr_price}")
    except:
        await message.answer("Введена некорректная криптовалюта")

    await state.clear()


@user_private_router.message(Command("help"))
async def about(message: types.Message):
    link_text = "Андрианов Артём"
    url = "t.me/ArtemkaAndrianov"
    await message.answer(
        f"Техподдержка:\n\nЕсли при использовании бота возникла\nошибка, пишите в личные сообщения\n[{link_text}]({url})",
        parse_mode="Markdown",
    )


@user_private_router.message(Command("stop"))
async def stop(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()

    if item[2] != 0:
        # await message.answer(
        #     "Чтобы прекратить отслеживание,\nвыберите кнопку:",
        #     reply_markup=create_delete_keyboard(message.from_user.id),
        # )
        await message.answer(
            "Выберите криптовалюту, которую вы\nбольше не хотите отслеживать:",
            reply_markup=create_delete_keyboard(message.from_user.id),
        )
    else:
        await message.answer(
            f"{message.from_user.first_name}, у вас не отслеживается ни одной криптовалюты\nдля начала отслеживания,\nиспользуйте команду '/adding_crypto'"
        )


@user_private_router.callback_query(
    lambda c: c.data in ["delete_all", "delete_first", "delete_second", "delete_third"]
)
async def on_delete_callback(callback_query: CallbackQuery):
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
            if item[3]:
                index_delete_all += "3_4;"
            if item[9]:
                index_delete_all += "9_10;"
            if item[15]:
                index_delete_all += "15_16;"

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
            await callback_query.message.answer(
                "Все криптовалюты успешно\nудалены из отслеживания!"
            )

        elif callback_query.data == "delete_first":
            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?, coin1_first = ?,
                    coin2_first = ?, short_window_first = ?, long_window_first = ?,
                    interval_first = ?, is_tracking_first = ? WHERE Id = ?""",
                (
                    curr_stop_flag + "3_4;",
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
            await callback_query.message.answer(
                f"Пара {item[3]}_{item[4]} успешно\nудалена из отслеживания!"
            )

        elif callback_query.data == "delete_second":
            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?, coin1_second = ?,
                    coin2_second = ?, short_window_second = ?, long_window_second = ?,
                    interval_second = ?, is_tracking_second = ? WHERE Id = ?""",
                (
                    curr_stop_flag + "9_10;",
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
            await callback_query.message.answer(
                f"Пара {item[9]}_{item[10]} успешно\nудалена из отслеживания!"
            )

        else:
            cursor.execute(
                """
                    UPDATE users_tracking SET stop_flag = ?, tracking_quantity = ?, coin1_third = ?,
                    coin2_third = ?, short_window_third = ?, long_window_third = ?,
                    interval_third = ?, is_tracking_third = ? WHERE Id = ?""",
                (
                    curr_stop_flag + "15_16;",
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
            await callback_query.message.answer(
                f"Пара {item[15]}_{item[16]} успешно\nудалена из отслеживания!"
            )

    conn.commit()
    conn.close()


class Form_create_demo_account(StatesGroup):
    waiting_for_message_create_demo_account = State()
    waiting_for_message_set_operation_percent = State()


@user_private_router.message(Command("open_demo_account"))
async def open_demo_account(message: types.Message, state: FSMContext):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_demo_account FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    is_demo_account = cursor.fetchone()
    conn.close()
    if not is_demo_account:
        is_demo_account = "False"
    else:
        is_demo_account = is_demo_account[0]

    if is_demo_account == "False":
        await state.set_state(
            Form_create_demo_account.waiting_for_message_create_demo_account
        )
        await message.answer(
            "Введите сумму в $ для создания демо-счёта\nВвод в формате целого числа!"
        )

    else:
        await message.answer("У вас уже создан демо-счёт!")


@user_private_router.message(
    Form_create_demo_account.waiting_for_message_create_demo_account
)
async def process_message_create_demo_account(
    message: types.Message, state: FSMContext
):
    try:
        start_sum = int(message.text)
        sucsess = True
    except:
        await message.answer(
            "Ошибка ввода данных!\nCумма должна быть целым числом,\nбез лишних символов"
        )
        sucsess = False

    if sucsess:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()

        cursor.execute(
            """
                UPDATE users_demo_account SET is_demo_account = ?, start_sum = ?, current_sum = ?
                WHERE Id = ?
                """,
            (
                "True",
                start_sum,
                start_sum,
                message.from_user.id,
            ),
        )

        conn.commit()
        conn.close()

        await message.answer(
            """Демо-счёт успешно создан!

Хотите ли вы, чтобы бот автоматически
торговал на вашем демо-счёте,
используя свои сигналы на валюты,
находящиеся в отслеживании?""",
            reply_markup=create_is_auto_operation_keyboard(),
        )

    await state.clear()


@user_private_router.callback_query(
    lambda c: c.data in ["is_auto_operation_True", "is_auto_operation_False"]
)
async def is_auto_operation_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "is_auto_operation_True":
        await state.set_state(
            Form_create_demo_account.waiting_for_message_set_operation_percent
        )
        await callback_query.message.answer(
            "Введите процент от общей суммы,\nна который будет покупаться\nкриптовалюта, при сигналах\nна покупку"
        )

    else:
        await callback_query.message.answer("Хорошо")


@user_private_router.message(
    Form_create_demo_account.waiting_for_message_set_operation_percent
)
async def process_message_set_operation_percent(
    message: types.Message, state: FSMContext
):
    try:
        operation_percent = int(message.text)
        sucsess = True
    except:
        await message.answer(
            "Ошибка ввода данных!\nпроцент должен быть целым числом от 1 до 100, без лишних символов"
        )
        sucsess = False

    if sucsess and (operation_percent < 1 or operation_percent > 100):
        await message.answer(
            "Ошибка ввода данных!\nпроцент должен быть целым числом от 1 до 100, без лишних символов"
        )
        sucsess = False

    if sucsess:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()

        cursor.execute(
            """
                UPDATE users_demo_account SET is_auto_operation = ?, operation_percent = ?
                WHERE Id = ?
                """,
            (
                "True",
                operation_percent,
                message.from_user.id,
            ),
        )

        conn.commit()
        conn.close()

        await message.answer(
            f"Процент успешно установлен!\nТекущий процент: {operation_percent}%"
        )

    await state.clear()


@user_private_router.message(Command("close_demo_account"))
async def close_demo_account(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_demo_account FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    is_demo_account = cursor.fetchone()
    conn.close()
    if not is_demo_account:
        is_demo_account = "False"
    else:
        is_demo_account = is_demo_account[0]

    if is_demo_account == "True":
        await message.answer(
            "Вы уверены, что хотите закрыть демо-счёт?",
            reply_markup=create_is_close_demo_account_keyboard(),
        )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")


@user_private_router.callback_query(
    lambda c: c.data in ["is_close_demo_account_True", "is_close_demo_account_False"]
)
async def is_close_demo_account_callback(callback_query: CallbackQuery):
    if callback_query.data == "is_close_demo_account_True":
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE users_demo_account SET is_demo_account = ?, start_sum = ?,
                current_sum = ?, is_auto_operation = ?, operation_percent = ?
                WHERE Id = ?
                """,
            (
                "False",
                0,
                0,
                "False",
                0,
                callback_query.from_user.id,
            ),
        )
        conn.commit()
        conn.close()

        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        cursor_currency.execute(
            f"DROP TABLE IF EXISTS {'user' + str(callback_query.from_user.id)}"
        )
        conn_currency.commit()
        conn_currency.close()

        await callback_query.message.answer(
            "Демо-счёт успешно закрыт, но вы по-прежнему можете открыть новый"
        )
    else:
        await callback_query.message.answer(
            "Хорошо, вы по-преженему можете использовать текущий демо-счёт"
        )


@user_private_router.message(Command("demo_account_transaction"))
async def demo_account_transaction(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_demo_account FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    is_demo_account = cursor.fetchone()
    conn.close()
    if not is_demo_account:
        is_demo_account = "False"
    else:
        is_demo_account = is_demo_account[0]

    if is_demo_account == "True":
        await message.answer(
            "Вы хотите положить деньги на демо-счёт или снять?",
            reply_markup=create_demo_account_transaction_keyboard(),
        )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")


class Form_demo_account_transaction(StatesGroup):
    waiting_for_message_add_demo_account = State()
    waiting_for_message_subtract_demo_account = State()


@user_private_router.callback_query(
    lambda c: c.data in ["add_demo_account", "subtract_demo_account"]
)
async def demo_account_transaction_callback(
    callback_query: CallbackQuery, state: FSMContext
):
    if callback_query.data == "add_demo_account":
        await state.set_state(
            Form_demo_account_transaction.waiting_for_message_add_demo_account
        )
        await callback_query.message.answer(
            "Введите сумму, которую хотите добавить на свой демо-счёт.\n\nВ формате целого числа, без лишних символов!"
        )
    else:
        await state.set_state(
            Form_demo_account_transaction.waiting_for_message_subtract_demo_account
        )
        await callback_query.message.answer(
            "Введите сумму, которую хотите снять со своего демо-счёта.\n\nВ формате целого числа, без лишних символов!"
        )


@user_private_router.message(
    Form_demo_account_transaction.waiting_for_message_add_demo_account
)
async def process_message_add_demo_account(message: types.Message, state: FSMContext):
    try:
        add_sum = int(message.text)
        sucsess = True
    except:
        await message.answer(
            "Ошибка ввода данных!\nCумма должна быть целым числом,\nбез лишних символов"
        )
        sucsess = False

    if sucsess:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT current_sum FROM users_demo_account WHERE Id = ?",
            (message.from_user.id,),
        )
        current_sum = cursor.fetchone()[0] + add_sum

        cursor.execute(
            """
                UPDATE users_demo_account SET current_sum = ? WHERE Id = ?
                """,
            (
                current_sum,
                message.from_user.id,
            ),
        )

        conn.commit()
        conn.close()

        await message.answer(f"На ваш демо-счёт успешно добавлено {add_sum}$")

    await state.clear()


@user_private_router.message(
    Form_demo_account_transaction.waiting_for_message_subtract_demo_account
)
async def process_message_subtract_demo_account(
    message: types.Message, state: FSMContext
):
    try:
        subtract_sum = int(message.text)
        sucsess = True
    except:
        await message.answer(
            "Ошибка ввода данных!\nCумма должна быть целым числом,\nбез лишних символов"
        )
        sucsess = False

    if sucsess:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT current_sum FROM users_demo_account WHERE Id = ?",
            (message.from_user.id,),
        )
        current_sum_data_base = cursor.fetchone()[0]

        if current_sum_data_base < subtract_sum:
            await message.answer(
                f"На вашем демо-счёте недостаточно средств для списания!\nСейчас у вас {current_sum_data_base}$"
            )
        else:
            current_sum = current_sum_data_base - subtract_sum
            cursor.execute(
                """
                    UPDATE users_demo_account SET current_sum = ? WHERE Id = ?
                    """,
                (
                    current_sum,
                    message.from_user.id,
                ),
            )

            await message.answer(f"С вашего демо-счёта успешно списано {subtract_sum}$")

        conn.commit()
        conn.close()

    await state.clear()


@user_private_router.message(Command("view_demo_account"))
async def view_demo_account(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_demo_account FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    is_demo_account = cursor.fetchone()
    if not is_demo_account:
        is_demo_account = "False"
    else:
        is_demo_account = is_demo_account[0]

    if is_demo_account == "True":
        cursor.execute(
            """SELECT start_sum, current_sum, is_auto_operation,
            operation_percent FROM users_demo_account WHERE Id = ?""",
            (message.from_user.id,),
        )
        demo_account_info = cursor.fetchone()
        text_message = f"Ваш демо-счёт:\n\nСумма открытия: {demo_account_info[0]}$\nТекущая сумма: {demo_account_info[1]}$\n"
        if demo_account_info[2] == "True":
            text_message += f"Автоматические операции по вкладу включены\nПроцент для автоматических операций: {demo_account_info[3]}%"
        else:
            text_message += "Автоматические операции по вкладу отключены"
        
        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        table_name = "user" + str(message.from_user.id)
        cursor_currency.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (table_name,))
        
        if cursor_currency.fetchone():
            cursor_currency.execute(
                f"SELECT * FROM {table_name}"
            )
            items = cursor_currency.fetchall()
            conn_currency.commit()
            conn_currency.close()

            if items:
                text_message += "\n\nВаши криптовалюты:"
                for item in items:
                    text_message += f"\n{item[0]}: {round(float(item[1]), 5)} шт."

        await message.answer(text_message)

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")

    conn.close()


@user_private_router.message(Command("update_demo_account"))
async def update_demo_account(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_demo_account FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    is_demo_account = cursor.fetchone()
    if not is_demo_account:
        is_demo_account = "False"
    else:
        is_demo_account = is_demo_account[0]

    if is_demo_account == "True":
        cursor.execute(
            "SELECT is_auto_operation FROM users_demo_account WHERE Id = ?",
            (message.from_user.id,),
        )

        if cursor.fetchone()[0] == "True":
            await message.answer(
                """Выберите действие для изменения настроек демо-счёта.
Если вы хотите изменить процент автоматических операций, нажмите 'Изменить';
если хотите отключить автоматические операции нажмите
'Отключить'""",
                reply_markup=create_update_demo_account_keyboard(),
            )
        else:
            await message.answer(
                "У вас не установлены автоматические операции по демо-счёту, хотите ли вы установить их?",
                reply_markup=create_is_auto_operation_keyboard(),
            )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")

    conn.close()


@user_private_router.callback_query(lambda c: c.data == "disable_auto_operation")
async def demo_account_transaction_callback(callback_query: CallbackQuery):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE users_demo_account SET is_auto_operation = ?,
        operation_percent = ? WHERE Id = ?""",
        (
            "False",
            0,
            callback_query.from_user.id,
        ),
    )
    conn.commit()
    conn.close()

    await callback_query.message.answer(
        "Автоматические операции по демо-счёту успешно отключены!"
    )
