import sqlite3, krakenex
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Keyboards.inline_buttons import MyCallback, create_keyboard, create_delete_keyboard
from Parsers_aio.Main_info_crypto_parser import General
from Parsers_aio.Item_info_crypto_parser import Crypto


user_private_router = Router()


# Определяем состояния
class Form_start_tracking(StatesGroup):
    waiting_for_message_start_tracking = State()


class Form_crypto_cap(StatesGroup):
    waiting_for_message_crypto_cap = State()


class Form_crypto_price(StatesGroup):
    waiting_for_message_crypto_price = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):

    # Подключение к базе данных
    conn = sqlite3.connect("Data_base.db")
    # Создание курсора
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()
    if not item:
        await message.reply(
            f"Привет, {message.from_user.first_name}, я твой виртуальный крипто помощник.",
            reply_markup=create_keyboard(),
        )
        cursor.execute(
            """
            INSERT OR IGNORE INTO users (
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

        # Сохранение изменений и закрытие
        conn.commit()

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
                    UPDATE users SET stop_flag = ?, tracking_quantity = ?, coin1_first = ?, coin2_first = ?, short_window_first = ?, long_window_first = ?, interval_first = ?, is_tracking_first = ?,
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

        await message.reply(
            "Перезапуск прошёл успешно!\nВсе криптовалюты удалены из отслеживания",
            reply_markup=create_keyboard(),
        )
        conn.commit()

    conn.close()


@user_private_router.callback_query(MyCallback.filter(F.foo == "start_tracking"))
async def my_callback_foo(query: CallbackQuery):

    await query.message.answer(
        text="Для начала отслеживания введи команду '/adding_crypto'"
    )


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
    try:
        text = str(message.text).split(",")
        coin1 = text[0].strip().upper()
        coin2 = text[1].strip().upper()
        short_window = int(text[2].strip())
        long_window = int(text[3].strip())
        interval = int(text[4].strip())
        sucsess = True
    except:
        sucsess = False

    if (
        sucsess
        and krakenex.API().query_public(
            "OHLC", {"pair": f"{coin1}{coin2}", "interval": interval}
        )["error"]
    ):
        sucsess = False

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tracking_quantity FROM users")
    items = cursor.fetchall()
    conn.close()
    sum_items = 0
    for i in items:
        sum_items += i[0]
    if sum_items < 15:
        if sucsess:
            conn = sqlite3.connect("Data_base.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE Id = ?", (message.from_user.id,))
            item = cursor.fetchone()

            if item[2] > 2:
                limit = False
            else:
                limit = True
                tracking_quantity = item[2] + 1

            if item[8] == "False" and limit:
                cursor.execute(
                    """
                    UPDATE users SET tracking_quantity = ?, coin1_first = ?, coin2_first = ?, short_window_first = ?, long_window_first = ?, interval_first = ?, is_tracking_first = ? WHERE Id = ?""",
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

            elif item[14] == "False" and limit:
                cursor.execute(
                    """
                    UPDATE users SET tracking_quantity = ?, coin1_second = ?, coin2_second = ?, short_window_second = ?, long_window_second = ?, interval_second = ?, is_tracking_second = ? WHERE Id = ?""",
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

            elif item[20] == "False" and limit:
                cursor.execute(
                    """
                    UPDATE users SET tracking_quantity = ?, coin1_third = ?, coin2_third = ?, short_window_third = ?, long_window_third = ?, interval_third = ?, is_tracking_third = ? WHERE Id = ?""",
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
            else:
                await message.answer(
                    "Слишком много криптовалют\nбыло добавлено\nлимит: 3"
                )

            conn.commit()
            conn.close()
            if limit:
                await message.answer("Успех!!!")
        else:
            await message.answer("Неудача")
    else:
        await message.answer(
            "Нет свободных мест на отслеживание,\nлимит на всех пользователей: 15"
        )

    await state.clear()


@user_private_router.message(Command("profile"))
async def profile(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()
    message_text = (
        "Профиль:\n\nКриптовалют отслеживается:\n" + str(item[2]) + " из 3.\n\n"
    )

    if item[2] != 0:
        if item[2] == 3:
            message_text += f"1) {item[3]} в {item[4]},\nпараметр короткой скользящей средней = {item[5]},\nпараметр длинной скользящей средней = {item[6]},\nдлительность свечи в минутах = {item[7]};\n\n"
            message_text += f"2) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи в минутах = {item[13]};\n\n"
            message_text += f"3) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи в минутах = {item[19]};\n\n"

        elif item[2] == 1:
            if item[8] != "False":
                message_text += f"1) {item[3]} в {item[4]},\nпараметр короткой скользящей средней = {item[5]},\nпараметр длинной скользящей средней = {item[6]},\nдлительность свечи в минутах = {item[7]};\n\n"
            elif item[14] != "False":
                message_text += f"1) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи в минутах = {item[13]};\n\n"
            else:
                message_text += f"1) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи в минутах = {item[19]};\n\n"

        else:
            if item[8] == "False":
                message_text += f"1) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи в минутах = {item[13]};\n\n"
                message_text += f"2) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи в минутах = {item[19]};\n\n"
            else:
                message_text += f"1) {item[3]} в {item[4]},\nпараметр короткой скользящей средней = {item[5]},\nпараметр длинной скользящей средней = {item[6]},\nдлительность свечи в минутах = {item[7]};\n\n"
                if item[14] == "False":
                    message_text += f"2) {item[15]} в {item[16]},\nпараметр короткой скользящей средней = {item[17]},\nпараметр длинной скользящей средней = {item[18]},\nдлительность свечи в минутах = {item[19]};\n\n"
                else:
                    message_text += f"2) {item[9]} в {item[10]},\nпараметр короткой скользящей средней = {item[11]},\nпараметр длинной скользящей средней = {item[12]},\nдлительность свечи в минутах = {item[13]};\n\n"

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
стоимость конкретной криптовалюты;"""
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
        await message.answer(
            f"Рыночная капитализация {curr_name}:\n$ {curr_capitalization}"
        )
    except:
        await message.answer("Введена некорректная криптовалюта")

    await state.clear()


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
    cursor.execute("SELECT * FROM users WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()

    if item[2] != 0:
        await message.answer(
            "Чтобы прекратить отслеживание,\nвыберите кнопку:",
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

    cursor.execute("SELECT * FROM users WHERE Id = ?", (callback_query.from_user.id,))
    item = cursor.fetchone()

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
                    UPDATE users SET stop_flag = ?, tracking_quantity = ?, coin1_first = ?, coin2_first = ?, short_window_first = ?, long_window_first = ?, interval_first = ?, is_tracking_first = ?,
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
                    UPDATE users SET stop_flag = ?, tracking_quantity = ?, coin1_first = ?, coin2_first = ?, short_window_first = ?, long_window_first = ?, interval_first = ?, is_tracking_first = ? WHERE Id = ?""",
                (
                    "3_4;",
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
                    UPDATE users SET stop_flag = ?, tracking_quantity = ?, coin1_second = ?, coin2_second = ?, short_window_second = ?, long_window_second = ?, interval_second = ?, is_tracking_second = ? WHERE Id = ?""",
                (
                    "9_10;",
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
                    UPDATE users SET stop_flag = ?, tracking_quantity = ?, coin1_third = ?, coin2_third = ?, short_window_third = ?, long_window_third = ?, interval_third = ?, is_tracking_third = ? WHERE Id = ?""",
                (
                    "15_16;",
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
