# in venv:
# python -m pip install requests, BeautifulSoup4, transliterate, langdetect
# if not work:
# py -m pip install requests, BeautifulSoup4, transliterate, langdetect


import requests
from bs4 import BeautifulSoup
from time import time, sleep
from urllib.parse import urljoin
from static_for_all import *
from transliterate import translit
from langdetect import detect


class General:

    def get_data_market_capitalization():
        data_market_capitalization = (
            soup.find(
                "div",
                class_="tw-font-bold tw-text-gray-900 dark:tw-text-moon-50 tw-text-lg tw-leading-7",
            )
            .text.replace("\n", "")
            .replace("$", "")
        )
        sleep(0.5)
        return data_market_capitalization

    def get_change_market_capitalization():

        decrease_in_capitalization = ".gecko-up{--tw-text-opacity:1;color:rgb(0 168 62/var(--tw-text-opacity))}:is(.tw-dark .gecko-up){--tw-text-opacity:1;color:rgb(50 202 91/var(--tw-text-opacity))}.gecko-down{--tw-text-opacity:1;color:rgb(255 58 51/var(--tw-text-opacity))}"
        url_css = (
            "https://static.coingecko.com/packs/css/v2/application-c86563d7.chunk.css"
        )
        responce_css = requests.get(url_css, headers=headers)
        soup_css = str(BeautifulSoup(responce_css.text, "lxml"))
        if float(soup.find("span", class_="gecko-down").text.replace("%", "")) < float(
            soup.find("span", class_="gecko-up").text.replace("%", "")
        ):
            change_market_capitalization_value = soup.find(
                "span", class_="gecko-down"
            ).text
            sleep(0.5)
            return f"Рыночная капитализация криптовалюты снизилась на {change_market_capitalization_value}"
        else:
            change_market_capitalization_value = soup.find(
                "span", class_="gecko-up"
            ).text
            sleep(0.5)
            return f"Рыночная капитализация криптовалюты увеличилась на {change_market_capitalization_value}"

    def get_total_trading_volume_per_day():
        total_trading_volume_per_day = (
            soup.find(
                "div",
                class_="tw-flex tw-flex-col tw-gap-2",
            )
            .find_all(
                "div",
                class_="tw-font-bold tw-text-gray-900 dark:tw-text-moon-50 tw-text-lg tw-leading-7",
            )[1]
            .find("span")
            .text.replace("\n", "")
            .replace("$", "")
        )
        sleep(0.5)
        return total_trading_volume_per_day


class Crypto:

    def __init__(self, crypto_name):
        self.__crypto_name = self.__is_valid_crypto_name(crypto_name)
        self.__url_crypto = (
            "https://bitinfocharts.com/ru/" + self.__crypto_name.lower() + "/"
        )
        self.__responce_crypto = requests.get(self.__url_crypto)
        self.__soup_crypto = BeautifulSoup(self.__responce_crypto.text, "lxml")

    def __is_valid_crypto_name(self, crypto_name):
        if str(detect(crypto_name)) != "fi":
            crypto_name = (
                str(translit(crypto_name, language_code="ru", reversed=True))
                .replace("koin", "coin")
                .replace("kesh", "cash")
                .lower()
            )
        else:
            crypto_name.lower()

        is_valid = requests.get(
            "https://bitinfocharts.com/ru/" + crypto_name.lower() + "/"
        ).text
        soup_is_valid = str(BeautifulSoup(is_valid, "lxml").find("h1").text)
        if soup_is_valid == "404 Not Found":
            raise ValueError
        else:
            return crypto_name

    @property
    def get_crypto_name(self):
        return self.__crypto_name.lower()

    def get_current_average_crypto_price(self):
        count = 0
        current_crypto_price = None
        while True:
            try:
                current_crypto_price = (
                    self.__soup_crypto.find("td", id=f"tdid{count}")
                    .find("a")
                    .find("span")
                    .find("span")
                    .text.replace(",", " ")
                )
            except:
                count += 1
                sleep(0.5)
                continue
            break

        return current_crypto_price

    def get_current_crypto_capitalization(self):
        try:
            current_crypto_capitalization = (
                self.__soup_crypto.find(attrs={"style": "font-weight:bold"})
                .text.replace("$", "")
                .replace(",", " ")
            )
        except:
            current_crypto_capitalization = "Нет информации"
        sleep(0.5)
        return current_crypto_capitalization


class Additional_CoinGecko_info:

    def __init__(self):
        self.general_divs = soup.find_all(
            "div",
            class_="tw-max-w-[92vw] tw-ring-gray-200 dark:tw-ring-moon-700 tw-ring-2 tw-py-1.5 tw-px-2 tw-rounded-xl",
        )

    def get_popular_crypto(self):
        class_popular_crypto = self.general_divs[0].find_all(
            "div",
            class_="tw-flex tw-justify-between tw-px-2 tw-py-2.5 hover:tw-bg-gray-50 tw-rounded-lg dark:hover:tw-bg-moon-700",
        )
        dict_popular_crypto = {}
        for item in class_popular_crypto:
            new_item = (
                item.find(
                    "span",
                    class_="tw-text-gray-700 dark:tw-text-moon-100 tw-font-semibold tw-text-sm tw-leading-5",
                )
                .text.replace("\n", "")
                .strip()
            )
            dict_popular_crypto[new_item] = new_item
        return dict_popular_crypto


print(
    f"Рыночная капитализация криптовалюты = {General.get_data_market_capitalization()}$"
)

print(General.get_change_market_capitalization())

print(f"Общий объём торгов за 24 часа - {General.get_total_trading_volume_per_day()}$")

name_crypto = "БиТкоин кэш"
try:
    My_crypto = Crypto(name_crypto)
    print(
        f"Текущая средняя стоимость {My_crypto.get_crypto_name} = {My_crypto.get_current_average_crypto_price()}$"
    )

    print(
        f"Рыночная капитализация {My_crypto.get_crypto_name} = {My_crypto.get_current_crypto_capitalization()}$"
    )
except:
    print("Некорректно введено название криптовалюты")


My_Additional_CoinGecko_info = Additional_CoinGecko_info()
dict = My_Additional_CoinGecko_info.get_popular_crypto()
print("Самые популярные криптовалюты:", end=" ")
for _ in dict:
    print(dict[_], end="; ")
