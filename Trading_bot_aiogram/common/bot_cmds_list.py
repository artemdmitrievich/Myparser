from aiogram.types import BotCommand


# Список команд
private = [
    BotCommand(command="start", description="Запуск | Перезапуск"),
    BotCommand(command="about", description="Информация о боте"),
    BotCommand(command="profile", description="Профиль"),
    BotCommand(
        command="adding_crypto", description="Добавить криптовалюту в отслеживание"
    ),
    BotCommand(command="stop", description="Прекратить отслеживание криптовалюты"),
    BotCommand(command="open_demo_account", description="Открыть демо-счёт"),
    BotCommand(command="close_demo_account", description="Закрыть демо-счёт"),
    BotCommand(command="view_demo_account", description="Просмотр демо-счёта"),
    BotCommand(
        command="update_demo_account", description="Изменить настройки демо-счёта"
    ),
    BotCommand(
        command="demo_account_transaction",
        description="Добавить операцию по демо-счёту",
    ),
    BotCommand(
        command="crypto_account_transaction",
        description="Добавить операцию по крипто-счёту",
    ),
    BotCommand(command="get_crypto_volatility", description="Узнать волатильность криптовалюты"),
    BotCommand(
        command="get_total_capitalization", description="Общая рыночная капитализация"
    ),
    BotCommand(command="get_total_trading_volume", description="Общий объём торгов"),
    BotCommand(
        command="get_crypto_capitalization", description="Капит. конкр. криптовалюты"
    ),
    BotCommand(command="get_crypto_price", description="Цена конкр. криптовалюты"),
    BotCommand(command="command_list", description="Полный список команд с описанием"),
    BotCommand(command="help", description="Техподдержка"),
]
