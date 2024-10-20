# Установка необходимых пакетов для запуска программы
# in venv:
# python -m pip install requests, BeautifulSoup4, transliterate, langdetect
# if not work:
# py -m pip install requests, BeautifulSoup4, transliterate, langdetect

# Импорт необходимых классов парсеров
from Main_info_crypto_parser import General, Additional_CoinGecko_info
from Item_info_crypto_parser import Crypto
from Auto_Yobit_parser import start_tracking_crypto


# Вывод рыночной капитализация криптовалюты
print(
    f"Рыночная капитализация криптовалюты = {General.get_data_market_capitalization()}$"
)

# Вывод изменения рыночной капитализация криптовалюты за 24 часа
print(General.get_change_market_capitalization())

# Вывод общего объёма торгов за 24 часа
print(f"Общий объём торгов за 24 часа - {General.get_total_trading_volume_per_day()}$")


name_crypto = "БиТкоин кэш"  # Вводимое название криптовалюты
# Попытка создания экземпляра класса и дальнейших вызовов функций экземпляра класса
try:
    My_crypto = Crypto(name_crypto)

    # Вывод текущей средней стоимости введённой криптовалюты
    print(
        f"Текущая средняя стоимость {My_crypto.get_crypto_name} = {My_crypto.get_current_average_crypto_price()}$"
    )

    # Вывод рыночной капитализации введённой криптовалюты
    print(
        f"Рыночная капитализация {My_crypto.get_crypto_name} = {My_crypto.get_current_crypto_capitalization()}$"
    )
except:
    # Вывод в случае ошибки: "Некорректно введено название криптовалюты"
    print("Некорректно введено название криптовалюты")


# Вывод самых популярных криптовалют
My_Additional_CoinGecko_info = Additional_CoinGecko_info()
popular_crypto_dict = My_Additional_CoinGecko_info.get_popular_crypto()
print("Самые популярные криптовалюты:", end=" ")
for _ in popular_crypto_dict:
    print(popular_crypto_dict[_], end="; ")

# Переход на новую строку
print()

# Вывод криптовалют с самым большим ростом за 24 часа
greatest_growth_dict = My_Additional_CoinGecko_info.get_greatest_growth_crypto()
print("Самый большой рост у криптовалют:", end=" ")
for _ in greatest_growth_dict:
    print(greatest_growth_dict[_], end="; ")

# Запуск автоматического отслеживания криптовалюты
start_tracking_crypto(time_sleep=2)
