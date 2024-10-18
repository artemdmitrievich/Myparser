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
        sleep(1)
        return data_market_capitalization

    def get_change_market_capitalization():
        
        decrease_in_capitalization = (
            ".gecko-up{--tw-text-opacity:1;color:rgb(0 168 62/var(--tw-text-opacity))}:is(.tw-dark .gecko-up){--tw-text-opacity:1;color:rgb(50 202 91/var(--tw-text-opacity))}.gecko-down{--tw-text-opacity:1;color:rgb(255 58 51/var(--tw-text-opacity))}"
        )
        url_css = (
            "https://static.coingecko.com/packs/css/v2/application-c86563d7.chunk.css"
        )
        responce_css = requests.get(url_css, headers=headers)
        soup_css = str(BeautifulSoup(responce_css.text, "lxml"))
        sleep(1)
        if decrease_in_capitalization not in soup_css:
            change_market_capitalization_value = soup.find("span", class_="gecko-down").text
            return f"Рыночная капитализация криптовалюты снизилась на {change_market_capitalization_value}"
        else:
            change_market_capitalization_value = soup.find("span", class_="gecko-up").text
            return f"Рыночная капитализация криптовалюты увеличилась на {change_market_capitalization_value}"


class Crypto:

    def __init__(self, crypto_name):
        self.__crypto_name = (
            crypto_name
            if str(detect(crypto_name)) == "fi"
            else str(translit(crypto_name, language_code="ru", reversed=True))
            .replace("koin", "coin")
            .replace("kesh", "cash")
        )
        self.__url_crypto = (
            "https://bitinfocharts.com/ru/" + self.__crypto_name.lower() + "/"
        )
        self.__responce_crypto = requests.get(self.__url_crypto)
        self.__soup_crypto = BeautifulSoup(self.__responce_crypto.text, "lxml")

    def get_current_crypto_price(self):
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
                sleep(1)
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
        return current_crypto_capitalization


print(
    f"Рыночная капитализация криптовалюты = {General.get_data_market_capitalization()}$"
)

print(General.get_change_market_capitalization())

name_crypto = "биткоин кэш"
print(f"Стоимость {name_crypto} = {Crypto(name_crypto).get_current_crypto_price()}$")

print(
    f"Рыночная капитализация {name_crypto} = {Crypto(name_crypto).get_current_crypto_capitalization()}$"
)
