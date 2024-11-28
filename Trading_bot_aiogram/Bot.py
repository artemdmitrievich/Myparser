from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from Command_handlers.basic_commands import basic_commands_router
from Command_handlers.demo_account_commands import demo_account_commands_router
from Command_handlers.get_information_commands import get_info_commands_router
from Command_handlers.tracking_crypto_commands import tracking_crypto_commands_router
import os


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(basic_commands_router)
dp.include_router(demo_account_commands_router)
dp.include_router(get_info_commands_router)
dp.include_router(tracking_crypto_commands_router)


async def send_message(Id, message_text):
    await bot.send_message(chat_id=Id, text=message_text)
