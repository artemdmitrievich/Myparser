import sqlite3
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types.callback_query import CallbackQuery
from Keyboards.inline_buttons import (
    create_start_keyboard,
    create_restart_keyboard,
    MyCallback,
)
from Bot import bot


# Создание роутера
basic_commands_router = Router()


# Обработчик команды "/start"
@basic_commands_router.message(CommandStart())
async def start_cmd(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (message.from_user.id,))
    item = cursor.fetchone()

    # Если пользователь есть в базе данных
    if not item:
        await message.reply(
            f"Привет, {message.from_user.first_name}, я твой виртуальный крипто помощник.",
            reply_markup=create_start_keyboard(),
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
        conn.commit()

        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        cursor_currency.execute(
            f"DROP TABLE IF EXISTS {'user' + str(message.from_user.id)}"
        )
        conn_currency.commit()
        conn_currency.close()

    # Если пользователя нет в базе данных
    else:
        await message.answer(
            f"{message.from_user.first_name}, вы уверены, что хотите перезапустить бота? После перезапуска бот полностью обнулится, будто вы им никогда не пользовались",
            reply_markup=create_restart_keyboard(),
        )

    conn.close()


@basic_commands_router.callback_query(MyCallback.filter(F.foo == "start_tracking"))
async def my_callback_foo(query: CallbackQuery):
    await bot.answer_callback_query(query.id)

    await query.message.answer(
        text="Для начала отслеживания введи команду '/adding_crypto'"
    )


@basic_commands_router.callback_query(
    lambda c: c.data in ["restart_True", "restart_False"]
)
async def restart_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    if callback_query.data == "restart_True":
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users_tracking WHERE Id = ?",
            (callback_query.from_user.id,),
        )
        item = cursor.fetchone()

        if item[2] != 0:
            if item[1]:
                index_delete_all = item[1]
            else:
                index_delete_all = ""
            if item[3] and item[8] != "Waiting":
                index_delete_all += "3_4;"
            if item[9] and item[14] != "Waiting":
                index_delete_all += "9_10;"
            if item[15] and item[20] != "Waiting":
                index_delete_all += "15_16;"

            if index_delete_all != "":
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
                callback_query.from_user.id,
            ),
        )

        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        cursor_currency.execute(
            f"DROP TABLE IF EXISTS {'user' + str(callback_query.from_user.id)}"
        )
        conn_currency.commit()
        conn_currency.close()

        await callback_query.message.reply(
            "Перезапуск прошёл успешно!\nВсе криптовалюты удалены из отслеживания",
            reply_markup=create_start_keyboard(),
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
    else:
        await callback_query.message.answer("Хорошо")


# Обработчик команды "/about"
@basic_commands_router.message(Command("about"))
async def about(message: types.Message):
    await message.answer("Информация о боте:")


# Обработчик команды "/command_list"
@basic_commands_router.message(Command("command_list"))
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


# Обработчик команды "/help"
@basic_commands_router.message(Command("help"))
async def about(message: types.Message):
    link_text = "Андрианов Артём"
    url = "t.me/ArtemkaAndrianov"
    await message.answer(
        f"Техподдержка:\n\nЕсли при использовании бота возникла\nошибка, пишите в личные сообщения\n[{link_text}]({url})",
        parse_mode="Markdown",
    )
