import os
from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))


async def send_message(Id, message_text):
    await bot.send_message(chat_id=Id, text=message_text)
