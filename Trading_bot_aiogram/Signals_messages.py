# from Bot import bot

async def Sell_signal_message(query):
    # await bot.send_message(chat_id=user_id, text="Продавай!!!")
    await query.message.answer("Продавай")

async def Buy_signal_message(query):
    # await bot.send_message(chat_id=user_id, text="Покупай!!!")
    await query.message.answer("Покупай")