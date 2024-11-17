import sqlite3
from multiprocessing import Process
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Keyboards.inline_buttons import MyCallback, create_keyboard


user_private_router = Router()


# Определяем состояния
class Form(StatesGroup):
    waiting_for_message = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):

    await message.reply(
        f"Привет, {message.from_user.first_name}, я твой виртуальный крипто помощник.",
        reply_markup=create_keyboard(),
    )

    # Подключение к базе данных
    conn = sqlite3.connect("Data_base.db")
    # Создание курсора
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
                Id INTEGER PRIMARY KEY,
                stop_flag TEXT,
                tracking_quantity INTEGER,
                coin1_first TEXT,
                coin2_first TEXT,
                short_window_first INTEGER,
                long_window_first INTEGER,
                interval_first INTEGER,
                is_tracking_first TEXT,
                coin1_second TEXT,
                coin2_second TEXT,
                short_window_second INTEGER,
                long_window_second INTEGER,
                interval_second INTEGER,
                is_tracking_second TEXT,
                coin1_third TEXT,
                coin2_third TEXT,
                short_window_third INTEGER,
                long_window_third INTEGER,
                interval_third INTEGER,
                is_tracking_third TEXT
    )
"""
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
            "False",
            0,
            "None",
            "None",
            0,
            0,
            0,
            "False",
            "None",
            "None",
            0,
            0,
            0,
            "False",
            "None",
            "None",
            0,
            0,
            0,
            "False",
        ),
    )

    # Сохранение изменений и закрытие
    conn.commit()
    conn.close()


@user_private_router.callback_query(MyCallback.filter(F.foo == "start_tracking"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback, state: FSMContext):

    await query.message.answer(text="Для начала отслеживания введи команду '/adding_crypto'")    


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
        coin1 = text[0].strip()
        coin2 = text[1].strip()
        short_window = int(text[2].strip())
        long_window = int(text[3].strip())
        interval = int(text[4].strip())
        sucsess = True
    except:
        sucsess = False
    
    if sucsess:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users SET tracking_quantity = ?, coin1_first = ?, coin2_first = ?, short_window_first = ?, long_window_first = ?, interval_first = ? WHERE Id = ?""",
            (1, coin1, coin2, short_window, long_window, interval, message.from_user.id),
        )
        conn.commit()
        conn.close()
        await message.answer("Успех!!!")
    else:
        await message.answer("Неудача")

    await state.clear()


@user_private_router.message(Command("about"))
async def about(message: types.Message):
    await message.answer("Информация о боте")


@user_private_router.message(Command("stop"))
async def stop(message: types.Message):
    await message.answer("Прекращено отслеживание криптовалюты")
