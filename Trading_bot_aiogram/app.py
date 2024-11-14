import asyncio
from Bot import bot
from aiogram import Dispatcher, types
from user_private import user_private_router
from common.bot_cmds_list import private


ALLOWED_UPDATES = ['message, edit_message']

dp = Dispatcher()

dp.include_router(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())