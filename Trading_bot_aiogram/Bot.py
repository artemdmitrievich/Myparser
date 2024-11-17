from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from user_private import user_private_router
import os


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(user_private_router)


async def send_message(Id, message_text):
    await bot.send_message(chat_id=Id, text=message_text)