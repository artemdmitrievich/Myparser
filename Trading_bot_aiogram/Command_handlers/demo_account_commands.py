import sqlite3, krakenex, math
from time import sleep
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Keyboards.inline_buttons import (
    create_is_auto_operation_keyboard,
    create_is_close_demo_account_keyboard,
    create_demo_account_transaction_keyboard,
    create_update_demo_account_keyboard,
    create_crypto_account_transaction_keyboard,
    create_is_auto_operation_for_update_keyboard,
    create_is_stop_loss_keyboard,
    create_is_take_profit_keyboard
)
from Bot import bot, delete_message_after_delay
from Kraken_aio import MovingAverageCrossover
from asyncio import create_task


demo_account_commands_router = Router()


class Form_create_demo_account(StatesGroup):
    waiting_for_message_create_demo_account = State()
    waiting_for_message_set_operation_percent = State()


@demo_account_commands_router.message(Command("open_demo_account"))
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
            "Введите сумму в $ для создания демо-счёта\nВвод в формате числа!"
        )

    else:
        await message.answer("У вас уже создан демо-счёт!")


@demo_account_commands_router.message(
    Form_create_demo_account.waiting_for_message_create_demo_account
)
async def process_message_create_demo_account(
    message: types.Message, state: FSMContext
):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        start_sum = float(message.text)
    except:
        await message.answer(
            "Ошибка ввода данных!\nCумма должна быть целым числом,\nбез лишних символов"
        )
        return

    if start_sum < 1 or start_sum > 99999999999999:
        await message.answer(
            "Ошибка ввода данных!\nCумма не должна превышать 99999999999999$ или быть меньше 1$"
        )
        return

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

    await message.answer("Демо-счёт успешно создан!")
    confirmation_message = await message.answer(
        """
Хотите ли вы, чтобы бот автоматически
торговал на вашем демо-счёте,
используя свои сигналы на валюты,
находящиеся в отслеживании?""",
        reply_markup=create_is_auto_operation_keyboard(),
    )

    create_task(
        delete_message_after_delay(
            chat_id=confirmation_message.chat.id,
            message_id=confirmation_message.message_id,
        )
    )


@demo_account_commands_router.callback_query(
    lambda c: c.data in ["is_auto_operation_True", "is_auto_operation_False"]
)
async def is_auto_operation_callback(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "is_auto_operation_True":
        await state.set_state(
            Form_create_demo_account.waiting_for_message_set_operation_percent
        )
        await callback_query.message.answer(
            "Для подключения автоматических\nопераций по демо-счёту,\nвведите процент от общей суммы,\nна который будет покупаться\nкриптовалюта, при сигналах\nна покупку"
        )
    else:
        await callback_query.message.answer(
            "Вы отказались подключать автоматические операции по демо-счёту"
        )


@demo_account_commands_router.message(
    Form_create_demo_account.waiting_for_message_set_operation_percent
)
async def process_message_set_operation_percent(
    message: types.Message, state: FSMContext
):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        operation_percent = int(message.text)
    except:
        await message.answer(
            "Ошибка ввода данных!\nпроцент должен быть целым числом от 1 до 100, без лишних символов"
        )
        return

    if operation_percent < 1 or operation_percent > 100:
        await message.answer(
            "Ошибка ввода данных!\nпроцент должен быть целым числом от 1 до 100, без лишних символов"
        )
        return

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

    cursor.execute(
        "SELECT stop_loss_percent, take_profit_percent FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    items = cursor.fetchone()

    conn.commit()
    conn.close()

    await message.answer(
        f"Процент успешно установлен!\nТекущий процент: {operation_percent}%"
    )

    if not items[0]:
        confirmation_message = await message.answer(
            "Хотите ли вы установить стоп-лоссы (в процентах)?",
            reply_markup=create_is_stop_loss_keyboard(),
        )

        await delete_message_after_delay(
            chat_id=confirmation_message.chat.id,
            message_id=confirmation_message.message_id,
            message_to_reply=message
        )
    elif not items[1]:
        confirmation_message = await message.answer(
            "Хотите ли вы установить тейк-профиты (в процентах)?",
            reply_markup=create_is_take_profit_keyboard()
        )

        await delete_message_after_delay(
            chat_id=confirmation_message.chat.id,
            message_id=confirmation_message.message_id,
            message_to_reply=message
        )


class Form_is_stop_loss(StatesGroup):
    waiting_for_message_stop_loss_percent = State()


@demo_account_commands_router.callback_query(
        lambda c: c.data in ["is_stop_loss_True", "is_stop_loss_False"]
)
async def is_stop_loss_callback(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )
    
    if callback_query.data == "is_stop_loss_True":
        await state.set_state(
            Form_is_stop_loss.waiting_for_message_stop_loss_percent
        )

        await callback_query.message.answer(
            "Введите процент для стоп-лоссов, в формате целого числа"
        )
    else:
        await callback_query.message.answer(
            "Вы отказались устанавливать стоп-лоссы"
        )

        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT take_profit_percent FROM users_demo_account WHERE Id = ?",
            (callback_query.message.from_user.id,),
        )
        take_profit = cursor.fetchone()
        conn.close()

        if not take_profit:
            confirmation_message = await callback_query.message.answer(
                "Хотите ли вы установить тейк-профиты (в процентах)?",
                reply_markup=create_is_take_profit_keyboard()
            )

            await delete_message_after_delay(
                chat_id=confirmation_message.chat.id,
                message_id=confirmation_message.message_id,
                message_to_reply=callback_query.message
            )
        else:
            if not take_profit[0]:
                confirmation_message = await callback_query.message.answer(
                "Хотите ли вы установить тейк-профиты (в процентах)?",
                reply_markup=create_is_take_profit_keyboard()
            )

            await delete_message_after_delay(
                chat_id=confirmation_message.chat.id,
                message_id=confirmation_message.message_id,
                message_to_reply=callback_query.message
            )
        

@demo_account_commands_router.message(
    Form_is_stop_loss.waiting_for_message_stop_loss_percent
)
async def process_message_is_stop_loss(message: types.Message, state: FSMContext):
    await state.clear()

    try:
        stop_loss_percent = int(message.text.strip())
    except:
        await message.answer(
            "Ошибка ввода данных, процент должен быть целым положительным числом!"
        )
        return
    if stop_loss_percent <= 0:
        await message.answer(
            "Ошибка, процент должен быть положительным!"
        )
        return
    
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE users_demo_account SET stop_loss_percent = ?
            WHERE Id = ?
            """,
        (
            stop_loss_percent,
            message.from_user.id,
        ),
    )
    conn.commit()
    conn.close()

    await message.answer(
        f"Успешно установлен стоп-лосс на {stop_loss_percent}%"
    )

    confirmation_message = await message.answer(
        "Хотите ли вы установить тейк-профиты (в процентах)?",
        reply_markup=create_is_take_profit_keyboard()
    )

    await delete_message_after_delay(
        chat_id=confirmation_message.chat.id,
        message_id=confirmation_message.message_id,
        message_to_reply=message
    )


class Form_is_take_profit(StatesGroup):
    waiting_for_message_take_profit_percent = State()


@demo_account_commands_router.callback_query(
        lambda c: c.data in ["is_take_profit_True", "is_take_profit_False"]
)
async def is_take_profit_callback(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "is_take_profit_True":
        await state.set_state(
            Form_is_take_profit.waiting_for_message_take_profit_percent
        )

        await callback_query.message.answer(
            "Введите процент для тейк-профитов, в формате целого числа"
        )
    else:
        await callback_query.message.answer(
            "Вы отказались устанавливать тейк-профиты"
        )


@demo_account_commands_router.message(
    Form_is_take_profit.waiting_for_message_take_profit_percent
)
async def process_message_is_take_profit(message: types.Message, state: FSMContext):
    await state.clear()

    try:
        take_profit_percent = int(message.text.strip())
    except:
        await message.answer(
            "Ошибка ввода данных, процент должен быть целым положительным числом!"
        )
        return
    if take_profit_percent <= 0:
        await message.answer(
            "Ошибка, процент должен быть положительным!"
        )
        return
    
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE users_demo_account SET take_profit_percent = ?
            WHERE Id = ?
            """,
        (
            take_profit_percent,
            message.from_user.id,
        ),
    )
    conn.commit()
    conn.close()

    await message.answer(
        f"Успешно установлен тейк-профит на {take_profit_percent}%"
    )
    

@demo_account_commands_router.message(Command("close_demo_account"))
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
        confirmation_message = await message.answer(
            "Вы уверены, что хотите закрыть демо-счёт?",
            reply_markup=create_is_close_demo_account_keyboard(),
        )

        create_task(
            delete_message_after_delay(
                chat_id=confirmation_message.chat.id,
                message_id=confirmation_message.message_id,
                message_to_reply=message,
            )
        )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")


@demo_account_commands_router.callback_query(
    lambda c: c.data in ["is_close_demo_account_True", "is_close_demo_account_False"]
)
async def is_close_demo_account_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "is_close_demo_account_True":
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE users_demo_account SET is_demo_account = ?, start_sum = ?,
                current_sum = ?, is_auto_operation = ?, operation_percent = ?,
                stop_loss_percent = ?, take_profit_percent = ?
                WHERE Id = ?
                """,
            (
                "False",
                0,
                0,
                "False",
                0,
                None,
                None,
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
            "Вы отказались закрывать демо-счёт"
        )


@demo_account_commands_router.message(Command("view_demo_account"))
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
        text_message = f"Ваш демо-счёт:\n\nСумма открытия: {round(demo_account_info[0], 5)}$\nТекущая сумма: {round(demo_account_info[1], 5)}$\n"
        if demo_account_info[2] == "True":
            text_message += f"Автоматические операции на демо-счёту включены\nПроцент для автоматических операций: {demo_account_info[3]}%"
        else:
            text_message += "Автоматические операции на демо-счёту отключены"

        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        table_name = "user" + str(message.from_user.id)
        cursor_currency.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (table_name,),
        )

        if cursor_currency.fetchone():
            cursor_currency.execute(f"SELECT * FROM {table_name}")
            items = cursor_currency.fetchall()
            conn_currency.commit()
            conn_currency.close()

            if items:
                waiting_message = await message.answer("Запрос обрабатывается...")
                text_message += "\n\nВаши криптовалюты:"
                summ_crypto = 0
                for item in items:
                    summ_crypto += (
                        MovingAverageCrossover(coin1=item[0]).current_coin1_price()
                        * item[1]
                    )
                    text_message += f"\n{item[0]}: {math.floor(float(item[1]) * 100000) / 100000} шт."
                    sleep(0.1)
                text_message += f"\n\nВ общей сложности у вас на демо-счёте криптовалют на сумму {round(summ_crypto, 5)}$"
                text_message += f"\nВсего на демо-счёте с учётом криптовалют у вас находится {round(demo_account_info[1] + summ_crypto, 5)}$"
                await waiting_message.delete()

        await message.answer(text_message)

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")

    conn.close()


@demo_account_commands_router.message(Command("update_demo_account"))
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
            confirmation_message = await message.answer(
                """Выберите действие для изменения настроек демо-счёта.
Если вы хотите изменить процент автоматических операций, нажмите 'Изменить';
если хотите отключить автоматические операции нажмите
'Отключить'""",
                reply_markup=create_update_demo_account_keyboard(),
            )
        else:
            confirmation_message = await message.answer(
                "У вас не установлены автоматические операции по демо-счёту, хотите ли вы установить их?",
                reply_markup=create_is_auto_operation_for_update_keyboard(),
            )

        create_task(
            delete_message_after_delay(
                chat_id=confirmation_message.chat.id,
                message_id=confirmation_message.message_id,
                message_to_reply=message,
            )
        )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")

    conn.close()


@demo_account_commands_router.callback_query(
    lambda c: c.data in ["disable_auto_operation", "is_auto_operation_True_for_update"]
)
async def demo_account_transaction_callback(
    callback_query: CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "disable_auto_operation":
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
    else:
        await state.set_state(
            Form_create_demo_account.waiting_for_message_set_operation_percent
        )
        await callback_query.message.answer(
            "Введите процент от общей суммы,\nна который будет покупаться\nкриптовалюта, при сигналах\nна покупку"
        )


@demo_account_commands_router.callback_query(
    lambda c: c.data
    in ["is_auto_operation_True_for_update", "is_auto_operation_False_for_update"]
)
async def is_auto_operation_callback(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "is_auto_operation_True_for_update":
        await state.set_state(
            Form_create_demo_account.waiting_for_message_set_operation_percent
        )
        await callback_query.message.answer(
            "Введите процент от общей суммы,\nна который будет покупаться\nкриптовалюта, при сигналах\nна покупку"
        )

    else:
        await callback_query.message.answer(
            "Вы отказались подключать автоматические операции по демо-счёту"
        )


@demo_account_commands_router.message(Command("demo_account_transaction"))
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
        confirmation_message = await message.answer(
            "Вы хотите положить деньги на демо-счёт или снять?",
            reply_markup=create_demo_account_transaction_keyboard(),
        )

        create_task(
            delete_message_after_delay(
                chat_id=confirmation_message.chat.id,
                message_id=confirmation_message.message_id,
                message_to_reply=message,
            )
        )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")


class Form_demo_account_transaction(StatesGroup):
    waiting_for_message_add_demo_account = State()
    waiting_for_message_subtract_demo_account = State()


@demo_account_commands_router.callback_query(
    lambda c: c.data in ["add_demo_account", "subtract_demo_account"]
)
async def demo_account_transaction_callback(
    callback_query: CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "add_demo_account":
        await state.set_state(
            Form_demo_account_transaction.waiting_for_message_add_demo_account
        )
        await callback_query.message.answer(
            "Введите сумму, которую хотите добавить на свой демо-счёт.\n\nВ формате числа, без лишних символов!"
        )
    else:
        await state.set_state(
            Form_demo_account_transaction.waiting_for_message_subtract_demo_account
        )
        await callback_query.message.answer(
            "Введите сумму, которую хотите снять со своего демо-счёта.\n\nВ формате числа, без лишних символов!"
        )


@demo_account_commands_router.message(
    Form_demo_account_transaction.waiting_for_message_add_demo_account
)
async def process_message_add_demo_account(message: types.Message, state: FSMContext):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        add_sum = float(message.text)
    except:
        await message.answer(
            "Ошибка ввода данных!\nCумма должна быть числом,\nбез лишних символов"
        )
        return

    if add_sum < 1 or add_sum > 99999999999999:
        await message.answer(
            "Ошибка ввода данных!\nCумма не должна превышать 99999999999999$ или быть меньше 1$"
        )
        return

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


@demo_account_commands_router.message(
    Form_demo_account_transaction.waiting_for_message_subtract_demo_account
)
async def process_message_subtract_demo_account(
    message: types.Message, state: FSMContext
):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        subtract_sum = float(message.text)
    except:
        await message.answer(
            "Ошибка ввода данных!\nCумма должна быть числом,\nбез лишних символов"
        )
        return

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


@demo_account_commands_router.message(Command("crypto_account_transaction"))
async def crypto_account_transaction(message: types.Message):
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
        confirmation_message = await message.answer(
            "Вы хотите купить валюту или продать?",
            reply_markup=create_crypto_account_transaction_keyboard(),
        )

        create_task(
            delete_message_after_delay(
                chat_id=confirmation_message.chat.id,
                message_id=confirmation_message.message_id,
                message_to_reply=message,
            )
        )

    else:
        await message.answer("Действие невозможно!\nУ вас нет демо-счёта")


class Form_crypto_account_transaction(StatesGroup):
    waiting_for_message_buy_crypto = State()
    waiting_for_message_sell_crypto = State()


@demo_account_commands_router.callback_query(
    lambda c: c.data in ["buy_crypto", "sell_crypto"]
)
async def crypto_account_transaction_callback(
    callback_query: CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "buy_crypto":
        await state.set_state(
            Form_crypto_account_transaction.waiting_for_message_buy_crypto
        )
        await callback_query.message.answer(
            "Введите криптовалюту и сумму, на которую вы хотите её купить, в качестве разделителя используйте запятую.\nПример: BTC, 40"
        )

    else:
        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        table_name = "user" + str(callback_query.from_user.id)
        cursor_currency.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        result = cursor_currency.fetchone()
        if result:
            await state.set_state(
                Form_crypto_account_transaction.waiting_for_message_sell_crypto
            )
            await callback_query.message.answer(
                "Введите криптовалюту и количество, которое вы хотите продать, в качестве разделителя используйте запятую.\nРазделитель целой и дробной части числа - '.'\nПример: BTC, 0.01234"
            )
        else:
            await callback_query.message.answer(
                "Действие невозможно!\nУ вас нет криптовалют на демо-счёте"
            )


@demo_account_commands_router.message(
    Form_crypto_account_transaction.waiting_for_message_buy_crypto
)
async def process_message_buy_crypto(message: types.Message, state: FSMContext):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        text = message.text.split(",")
        crypto_name = text[0].strip().upper()
        buy_sum = float(text[1])
    except:
        await message.answer("Неверный формат ввода данных!")
        return

    try:
        coin1 = crypto_name
        coin2 = "USD"
        interval = 1
        if krakenex.API().query_public(
            "OHLC", {"pair": f"{coin1}{coin2}", "interval": interval}
        )["error"]:
            await message.answer("Введено некорректное значение валюты!")
            return
    except:
        await message.answer("Введено некорректное значение валюты!")
        return

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT current_sum FROM users_demo_account WHERE Id = ?",
        (message.from_user.id,),
    )
    current_sum = cursor.fetchone()[0]

    if buy_sum <= current_sum:
        cursor.execute(
            "UPDATE users_demo_account SET current_sum = ? WHERE Id = ?",
            (
                current_sum - buy_sum,
                message.from_user.id,
            ),
        )
        conn.commit()
        conn.close()

        conn_currency = sqlite3.connect("users_currency_base.db")
        cursor_currency = conn_currency.cursor()
        cursor_currency.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {"user" + str(message.from_user.id)} (
                currency_name TEXT PRIMARY KEY,
                currency_quantity REAL,
                last_signal TEXT
            )
        """
        )

        response = krakenex.API().query_public("Ticker", {"pair": crypto_name + "USD"})
        current_crypto_price = float(
            response["result"][list(response["result"].keys())[0]]["c"][0]
        )

        cursor_currency.execute(
            f"SELECT currency_quantity, last_signal FROM {'user' + str(message.from_user.id)} WHERE currency_name = ?",
            (crypto_name,),
        )
        item_currency = cursor_currency.fetchone()
        if item_currency:
            cursor_currency.execute(
                f"""
                UPDATE {"user" + str(message.from_user.id)} SET currency_quantity = ?
                WHERE currency_name = ?
            """,
                (
                    item_currency[0] + buy_sum / current_crypto_price,
                    crypto_name,
                ),
            )
        else:
            cursor_currency.execute(
                f"INSERT INTO {'user' + str(message.from_user.id)} ("
                f"currency_name,"
                f"currency_quantity,"
                f"last_signal"
                f") VALUES (?, ?, ?)",
                (
                    crypto_name,
                    buy_sum / current_crypto_price,
                    None,
                ),
            )

        conn_currency.commit()
        conn_currency.close()

        await message.answer(
            f"Вы успешно купили {math.floor(buy_sum / current_crypto_price * 100000) / 100000} {crypto_name} на сумму {round(buy_sum, 5)}$ на своём демо-счёте!"
        )

    else:
        await message.answer(
            f"На вашем демо-счёте недостаточно средств для списания!\nСейчас у вас {current_sum}$"
        )


@demo_account_commands_router.message(
    Form_crypto_account_transaction.waiting_for_message_sell_crypto
)
async def process_message_sell_crypto(message: types.Message, state: FSMContext):
    await state.clear()

    if "/" in message.text:
        await message.answer(
            "Ошибка!\nВы ввели команду!\nВведите команду ещё раз или повторите свои последние действия"
        )
        return

    try:
        text = message.text.split(",")
        crypto_name = text[0].strip().upper()
        sell_amount = float(text[1])
    except:
        await message.answer("Неверный формат ввода данных!")
        return

    conn_currency = sqlite3.connect("users_currency_base.db")
    cursor_currency = conn_currency.cursor()
    cursor_currency.execute(
        f"SELECT currency_quantity FROM {'user' + str(message.from_user.id)} WHERE currency_name = ?",
        (crypto_name,),
    )
    item = cursor_currency.fetchone()

    if item:
        currency_quantity = item[0]
        if sell_amount <= currency_quantity:
            if (currency_quantity - sell_amount) >= 0.00001:
                cursor_currency.execute(
                    f"UPDATE {'user' + str(message.from_user.id)} SET currency_quantity = ? WHERE currency_name = ?",
                    (
                        currency_quantity - sell_amount,
                        crypto_name,
                    ),
                )
                is_all = False
            else:
                cursor_currency.execute(
                    f"DELETE FROM {'user' + str(message.from_user.id)} WHERE currency_name = ?",
                    (crypto_name,),
                )
                is_all = True

            conn_currency.commit()
            conn_currency.close()

            response = krakenex.API().query_public(
                "Ticker", {"pair": crypto_name + "USD"}
            )
            current_crypto_price = float(
                response["result"][list(response["result"].keys())[0]]["c"][0]
            )

            conn = sqlite3.connect("Data_base.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT current_sum FROM users_demo_account WHERE Id = ?",
                (message.from_user.id,),
            )
            current_sum = cursor.fetchone()[0]

            cursor.execute(
                "UPDATE users_demo_account SET current_sum = ? WHERE Id = ?",
                (
                    current_sum + float(sell_amount * current_crypto_price),
                    message.from_user.id,
                ),
            )
            conn.commit()
            conn.close()

            if is_all:
                await message.answer(
                    f"Вы успешно продали все {crypto_name} со своего демо-счёта на сумму {round(float(sell_amount * current_crypto_price), 5)}$"
                )
            else:
                await message.answer(
                    f"Вы успешно продали {sell_amount} {crypto_name} со своего демо-счёта на сумму {round(float(sell_amount * current_crypto_price), 5)}$"
                )

        else:
            await message.answer(
                f"У вас нет столько {crypto_name} на демо-счёте!\nСейчас у вас {currency_quantity} {crypto_name}"
            )
    else:
        await message.answer(f"У вас на демо-счёте нет {crypto_name}")
