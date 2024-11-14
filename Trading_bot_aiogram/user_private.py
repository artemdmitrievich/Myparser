from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
import sqlite3
from Keyboards.inline_buttons import MyCallback, create_keyboard
from aiogram.types.callback_query import CallbackQuery
from Kraken_Signals_aio import MovingAverageCrossover
user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):

    await message.reply(
        f"Привет, {message.from_user.first_name}, я твой виртуальный крипто помощник.",
        reply_markup=create_keyboard()
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
                coin1_second TEXT,
                coin2_second TEXT,
                short_window_second INTEGER,
                long_window_second INTEGER,
                interval_second INTEGER,
                coin1_third TEXT,
                coin2_third TEXT,
                short_window_third INTEGER,
                long_window_third INTEGER,
                interval_third INTEGER
    )
"""
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (
        Id, stop_flag, tracking_quantity,
        coin1_first, coin2_first, short_window_first, long_window_first, interval_first,
        coin1_second, coin2_second, short_window_second, long_window_second, interval_second,
        coin1_third, coin2_third, short_window_third, long_window_third, interval_third
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            message.from_user.id,
            "False",
            0,
            "None",
            "None",
            0,
            0,
            0,
            "None",
            "None",
            0,
            0,
            0,
            "None",
            "None",
            0,
            0,
            0,
        ),
    )

    # Сохранение изменений и закрытие
    conn.commit()
    conn.close()


@user_private_router.callback_query(MyCallback.filter(F.foo == "start_tracking"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    MovingAverageCrossover("btc", "usd", 20, 50, 1).run()



@user_private_router.message(Command("adding_crypto"))
async def adding_crypto(message: types.Message):
    await message.answer("Введите криптовалюту,\nчтобы добавить её в отслеживание")


@user_private_router.message(Command("about"))
async def about(message: types.Message):
    await message.answer("Информация о боте")


@user_private_router.message(Command("stop"))
async def stop(message: types.Message):
    await message.answer("Прекращено отслеживание криптовалюты")
