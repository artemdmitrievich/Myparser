from Bot import bot

async def Sell_signal_message(user_id):
    await bot.send_message(chat_id=user_id, text="Продавай!!!")

async def Buy_signal_message(user_id):
    await bot.send_message(chat_id=user_id, text="Покупай!!!")