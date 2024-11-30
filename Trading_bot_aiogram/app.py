import asyncio
from multiprocessing import Process
from aiogram import types, Dispatcher
from Bot import bot
from common.bot_cmds_list import private
from Tracking import StartTrackingCrypto
from on_start_update_data_base import on_start_update_data_base
from aiogram.fsm.storage.memory import MemoryStorage
from Command_handlers.basic_commands import basic_commands_router
from Command_handlers.demo_account_commands import demo_account_commands_router
from Command_handlers.get_information_commands import get_info_commands_router
from Command_handlers.tracking_crypto_commands import tracking_crypto_commands_router


ALLOWED_UPDATES = ["message, edit_message"]


storage = MemoryStorage()

dp = Dispatcher(storage=storage)
dp.include_router(basic_commands_router)
dp.include_router(demo_account_commands_router)
dp.include_router(get_info_commands_router)
dp.include_router(tracking_crypto_commands_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=private, scope=types.BotCommandScopeAllPrivateChats()
    )
    await on_start_update_data_base()
    process = Process(target=StartTrackingCrypto)
    process.start()
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
