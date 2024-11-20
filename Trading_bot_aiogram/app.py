import asyncio
from multiprocessing import Process
from aiogram import types
from Bot import bot, dp
from common.bot_cmds_list import private
from Tracking import StartTrackingCrypto
from on_start_update_data_base import on_start_update_data_base


ALLOWED_UPDATES = ['message, edit_message']


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await on_start_update_data_base()
    process = Process(target=StartTrackingCrypto)
    process.start()
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
