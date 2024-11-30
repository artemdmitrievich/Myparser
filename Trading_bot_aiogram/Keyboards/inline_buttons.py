import sqlite3
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    foo: str


# Клавиатура для команды "/start"
def create_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="start_tracking", callback_data=MyCallback(foo="start_tracking")
    )
    return builder.as_markup()


# Клавиатура для перезапуска бота
def create_restart_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data="restart_True")

    builder.button(text="Нет", callback_data="restart_False")

    return builder.as_markup()


# Клавиатура для команды "/stop"
def create_delete_keyboard(Id):
    builder = InlineKeyboardBuilder()

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_tracking WHERE Id = ?", (Id,))
    item = cursor.fetchone()
    conn.close()

    if item[2] != 0:
        if item[2] != 1:
            builder.button(text="Удалить все", callback_data="delete_all")

        if item[8] != "False":
            builder.button(
                text=f"Удалить {item[3]}_{item[4]}", callback_data="delete_first"
            )

        if item[14] != "False":
            builder.button(
                text=f"Удалить {item[9]}_{item[10]}", callback_data="delete_second"
            )

        if item[20] != "False":
            builder.button(
                text=f"Удалить {item[15]}_{item[16]}", callback_data="delete_third"
            )

        builder.adjust(1, 2)
    return builder.as_markup()


# Клавиатура для предложения автоматического отслеживания
def create_is_auto_operation_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data="is_auto_operation_True")

    builder.button(text="Нет", callback_data="is_auto_operation_False")

    return builder.as_markup()


# Клавиатура для подтверждения закрытия демо-счёта
def create_is_close_demo_account_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data="is_close_demo_account_True")

    builder.button(text="Нет", callback_data="is_close_demo_account_False")

    return builder.as_markup()


# Клавиатура для команды "/create_demo_account_transaction"
def create_demo_account_transaction_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Положить", callback_data="add_demo_account")

    builder.button(text="Снять", callback_data="subtract_demo_account")

    return builder.as_markup()


# Клавиатура для команды "/create_crypto_account_transaction"
def create_crypto_account_transaction_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Купить", callback_data="buy_crypto")

    builder.button(text="Продать", callback_data="sell_crypto")

    return builder.as_markup()


# Клавиатура для команды "/create_update_demo_account"
def create_update_demo_account_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить", callback_data="is_auto_operation_True")

    builder.button(text="Отключить", callback_data="disable_auto_operation")

    return builder.as_markup()
