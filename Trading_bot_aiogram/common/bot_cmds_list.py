from aiogram.types import BotCommand


private = [
    BotCommand(command='adding_crypto', description='Введите криптовалюту, чтобы добавить её в отслеживание'),
    BotCommand(command='about', description='Информация о боте'),
    BotCommand(command='stop', description = 'Прекращено отслеживание криптовалюты'),
]