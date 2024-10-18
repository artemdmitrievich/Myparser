# in venv:
# python -m pip install requests, BeautifulSoup4
# if not work:
# py -m pip install requests, BeautifulSoup4


import requests
from bs4 import BeautifulSoup
from time import time, sleep
from urllib.parse import urljoin
from static_for_all import *


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
        return data_market_capitalization

    def get_change_market_capitalization():
        change_market_capitalization_value = soup.find("span", class_="gecko-down").text
        decrease_in_capitalization = (
            ".gecko-down{--tw-text-opacity:1;color:rgb(255 58 51"
        )
        url_css = (
            "https://static.coingecko.com/packs/css/v2/application-c86563d7.chunk.css"
        )
        responce_css = requests.get(url_css, headers=headers)
        soup_css = str(BeautifulSoup(responce_css.text, "lxml"))
        if decrease_in_capitalization in soup_css:
            return f"Рыночная капитализация снизилась на {change_market_capitalization_value}"
        else:
            return f"Рыночная капитализация увеличилась на {change_market_capitalization_value}"


class Crypto:
    def get_current_crypto_price(crypto_name):
        url_crypto = "https://bitinfocharts.com/ru/" + crypto_name.lower() + "/"
        responce_crypto = requests.get(url_crypto)
        soup_crypto = BeautifulSoup(responce_crypto.text, "lxml")
        count = 0
        current_crypto_price = None
        while True:
            try:
                current_crypto_price = (
                    soup_crypto.find("td", id=f"tdid{count}")
                    .find("a")
                    .find("span")
                    .find("span")
                    .text
                )
            except:
                count += 1
                sleep(1)
                continue
            break

        return current_crypto_price


print(
    f"Рыночная капитализация криптовалюты = {General.get_data_market_capitalization()}$"
)

name_crypto = "bitcoin"
print(f"Стоимость {name_crypto} = {Crypto.get_current_crypto_price(name_crypto)}$")

print(General.get_change_market_capitalization())
