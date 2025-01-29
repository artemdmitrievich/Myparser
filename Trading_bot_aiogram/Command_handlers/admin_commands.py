import sqlite3
from aiogram import Router, types
from aiogram.filters import Command, Filter
from Bot import ADMIN_IDS, send_message, bot, delete_message_after_delay
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from Keyboards.inline_buttons import create_is_message_from_all_users_keyboard
from asyncio import create_task


class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message):
        return message.from_user.id in ADMIN_IDS


admin_commands_router = Router()
admin_commands_router.message.filter(IsAdmin())


@admin_commands_router.message(Command("get_users_quantity"))
async def get_users_quantity(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users_main_info")
    quantity = cursor.fetchone()[0]
    conn.close()

    await message.answer(f"Ботом пользуются {quantity} человек")


@admin_commands_router.message(Command("get_users_list"))
async def get_users_list(message: types.Message):
    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Id, username, first_name, last_name FROM users_main_info")
    users = cursor.fetchall()

    text_message = "Список пользователей:\n"

    for index, user in enumerate(users, start=1):
        name = ""

        if user[2]:
            name += f" {user[2]}"
        if user[3]:
            name += f" {user[3]}"

        if name == "" and user[1]:
            name = f"\n    @{user[1]}"
        else:
            name = f"\n   {name}"

        text_message += f"\n{index}) Id: {user[0]}{name};"

    if text_message != "":
        await message.answer(text_message)
    else:
        message.answer("Нет пользователей!")


@admin_commands_router.message(Command("message_from_all_users"))
async def message_from_all_users(message: types.Message):
    confirmation_message = await message.answer(
        f"{message.from_user.first_name}, вы уверены, что хотите написать сообщение всем пользователям?",
        reply_markup=create_is_message_from_all_users_keyboard(),
    )

    create_task(
        delete_message_after_delay(
            chat_id=confirmation_message.chat.id,
            message_id=confirmation_message.message_id,
            message_to_reply=message,
        )
    )


class Form_message_from_all_users(StatesGroup):
    waiting_for_message_from_all_users = State()


@admin_commands_router.callback_query(
    lambda c: c.data
    in ["is_message_from_all_users_True", "is_message_from_all_users_False"]
)
async def is_message_from_all_users_callback(
    callback_query: CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)

    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if callback_query.data == "is_message_from_all_users_True":
        await state.set_state(
            Form_message_from_all_users.waiting_for_message_from_all_users
        )

        await callback_query.message.answer(
            "Введите текст сообщения для отправки всем пользователям"
        )
    else:
        await callback_query.message.answer(
            "Вы отказались отправлять сообщение всем пользователям"
        )


@admin_commands_router.message(
    Form_message_from_all_users.waiting_for_message_from_all_users
)
async def process_message_from_all_users(message: types.Message, state: FSMContext):
    await state.clear()

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Id FROM users_main_info""")
    Ids = cursor.fetchall()
    conn.close()

    for Id in Ids:
        await send_message(int(Id[0]), message.text)

    # await send_message(1270674543, message.text)


class Form_get_user_info(StatesGroup):
    waiting_for_message_user_id = State()


@admin_commands_router.message(Command("get_user_info"))
async def get_user_info(message: types.Message, state: FSMContext):
    await state.set_state(Form_get_user_info.waiting_for_message_user_id)

    await message.answer("Введите Id пользователя")


@admin_commands_router.message(Form_get_user_info.waiting_for_message_user_id)
async def process_message_get_user_info(message: types.Message, state: FSMContext):
    await state.clear()

    try:
        Id = int(message.text)
    except:
        await message.answer("Некорректный ввод Id пользователя")
        return

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT username, first_name, last_name, is_bot,
        is_premium, language_code, url FROM users_main_info WHERE Id = ?""",
        (Id,),
    )
    user_info = cursor.fetchone()
    conn.close()

    if user_info:
        Id = int(message.text)
        username = user_info[0]
        first_name = user_info[1]
        last_name = user_info[2]
        is_bot = user_info[3]
        is_premium = user_info[4]
        language_code = user_info[5]
        url = user_info[6]

        if not username:
            username = "Не указано"
        if not first_name:
            first_name = "Не указано"
        if not last_name:
            last_name = "Не указана"
        if is_bot == "True":
            is_bot = "Да"
        else:
            is_bot = "Нет"
        if is_premium == "True":
            is_premium = "Да"
        else:
            is_premium = "Нет"
        if not url:
            url = "Нет"

        await message.answer(
            f"Id: {Id}\n"
            f"Имя пользователя: {username}\n"
            f"Имя: {first_name}\n"
            f"Фамилия: {last_name}\n"
            f"Это бот: {is_bot}\n"
            f"Есть премиум: {is_premium}\n"
            f"Язык интерфейса: {language_code}\n"
            f"URL: {url}",
        )
    else:
        await message.answer("Нет пользователя с таким Id")
