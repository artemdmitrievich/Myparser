from aiogram.types import BotCommand


private = [
    BotCommand(command='start', description = 'Запуск | Перезапуск'),
    BotCommand(command='about', description='Информация о боте'),
    BotCommand(command='profile', description = 'Профиль'),
    BotCommand(command='adding_crypto', description='Добавить криптовалюту в отслеживание'),
    BotCommand(command='stop', description = 'Прекратить отслеживание криптовалюты'),
    BotCommand(command='demo_account', description = 'Демо счёт для торговли'),
    BotCommand(command='get_total_capitalization', description = 'Общая рыночная капитализация'),
    BotCommand(command='get_total_trading_volume', description = 'Общий объём торгов'),
    BotCommand(command='get_crypto_capitalization', description = 'Капит. конкр. криптовалюты'),
    BotCommand(command='get_crypto_price', description = 'Цена конкр. криптовалюты'),
    BotCommand(command='command_list', description = 'Полный список команд с описанием'),
    BotCommand(command='help', description = 'Техподдержка'),
]