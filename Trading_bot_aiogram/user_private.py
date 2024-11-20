import sqlite3, krakenex
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Keyboards.inline_buttons import MyCallback, create_keyboard, create_delete_keyboard


user_private_router = Router()


# Определяем состояния
class Form(StatesGroup):
    waiting_for_message = State()


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
        await message.answer(
            "Перезапуск прошёл успешно!\nВсе криптовалюты удалены из отслеживания"
        )
        conn.commit()

    conn.close()


@user_private_router.callback_query(MyCallback.filter(F.foo == "start_tracking"))
async def my_callback_foo(
    query: CallbackQuery, callback_data: MyCallback, state: FSMContext
):

    await query.message.answer(
        text="Для начала отслеживания введи команду '/adding_crypto'"
    )


@user_private_router.message(Command("adding_crypto"))
async def adding_crypto(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_message)
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


@user_private_router.message(Form.waiting_for_message)
async def process_message(message: types.Message, state: FSMContext):
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
            await message.answer("Слишком много криптовалют\nбыло добавлено\nлимит: 3")

        conn.commit()
        conn.close()
        if limit:
            await message.answer("Успех!!!")
    else:
        await message.answer("Неудача")

    await state.clear()


@user_private_router.message(Command("profile"))
async def about(message: types.Message):
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
    await message.answer("Информация о боте")


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
            "У вас не отслеживается ни одной криптовалюты\nдля начала отслеживания,\nиспользуйте команду '/adding_crypto'"
        )


@user_private_router.callback_query(
    lambda c: c.data in ["delete_all", "delete_first", "delete_second", "delete_third"]
)
async def delete_callback_buttons(callback_query: CallbackQuery):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE Id = ?", (callback_query.from_user.id,))
    item = cursor.fetchone()

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
