import os
from dotenv import find_dotenv, load_dotenv
from aiogram import Bot
from asyncio import sleep


ADMIN_IDS = [1270674543]


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))


async def send_message(Id, message_text):
    await bot.send_message(chat_id=Id, text=message_text)


async def delete_message_after_delay(
    chat_id,
    message_id,
    message_to_reply=None,
    delay=60,
    after_delete_message="От вас не был получен ответ,\nвремя ожидания истекло!",
):
    await sleep(delay)

    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        if message_to_reply:
            await message_to_reply.reply(after_delete_message)
    except:
        pass
