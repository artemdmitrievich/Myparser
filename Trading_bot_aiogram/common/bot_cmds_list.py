from aiogram.types import BotCommand


private = [
    BotCommand(command='start', description = 'Запуск | Перезапуск'),
    BotCommand(command='about', description='Информация о боте'),
    BotCommand(command='profile', description = 'Профиль'),
    BotCommand(command='command_list', description = 'Полный список всех команд'),
    BotCommand(command='adding_crypto', description='Добавить криптовалюту в отслеживание'),
    BotCommand(command='stop', description = 'Прекратить отслеживание криптовалюты'),
    BotCommand(command='help', description = 'Техподдержка'),
]