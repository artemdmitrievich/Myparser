from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    foo: str

def create_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="start_tracking",
        callback_data=MyCallback(foo="start_tracking")
    )
    return builder.as_markup()