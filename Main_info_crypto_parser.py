import requests
from bs4 import BeautifulSoup
from time import time, sleep
from static.Soup_main_CoinGecko import soup
from static.headers import Headers


# Класс с общей информацией по криптовалюте
class General:

    # Получение общей капитализации криптовалюты
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

    # Получение изменения общей капитализации криптовалюты за 24 часа
    def get_change_market_capitalization():

        decrease_in_capitalization = ".gecko-up{--tw-text-opacity:1;color:rgb(0 168 62/var(--tw-text-opacity))}:is(.tw-dark .gecko-up){--tw-text-opacity:1;color:rgb(50 202 91/var(--tw-text-opacity))}.gecko-down{--tw-text-opacity:1;color:rgb(255 58 51/var(--tw-text-opacity))}"
        url_css = (
            "https://static.coingecko.com/packs/css/v2/application-c86563d7.chunk.css"
        )
        responce_css = requests.get(url_css, headers=Headers)
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

    # Получение общего объёма торгов за 24 часа
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


# Класс с дополнительной информацией по криптовалюте
class Additional_CoinGecko_info:

    def __init__(self):
        self.general_divs = soup.find_all(
            "div",
            class_="tw-max-w-[92vw] tw-ring-gray-200 dark:tw-ring-moon-700 tw-ring-2 tw-py-1.5 tw-px-2 tw-rounded-xl",
        )

    # Получение информации по 3 самым популярным криптовалютам за последние 3 часа по версии CoinGecko.com
    def get_popular_crypto(self):
        class_popular_crypto = self.general_divs[0].find_all(
            "div",
            class_="tw-flex tw-justify-between tw-px-2 tw-py-2.5 hover:tw-bg-gray-50 tw-rounded-lg dark:hover:tw-bg-moon-700",
        )
        dict_popular_crypto = {}
        for item in class_popular_crypto:
            name_item = (
                item.find(
                    "span",
                    class_="tw-text-gray-700 dark:tw-text-moon-100 tw-font-semibold tw-text-sm tw-leading-5",
                )
                .text.replace("\n", "")
                .strip()
            )
            price_item = (
                item.find(
                    "div",
                    class_="tw-flex tw-justify-end tw-items-center tw-flex-shrink-0 tw-max-w-[50%] tw-break-words tw-text-right",
                )
                .find("span")
                .find("span")
                .text.replace("$", "")
            )
            dict_popular_crypto[name_item] = name_item, price_item
        return dict_popular_crypto

    # Получение информации по 3 криптовалютам с самым большим ростом за последние 24 часа по версии CoinGecko.com
    def get_greatest_growth_crypto(self):
        class_popular_crypto = self.general_divs[1].find_all(
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
            price_item = (
                item.find(
                    "div",
                    class_="tw-flex tw-justify-end tw-items-center tw-flex-shrink-0 tw-max-w-[50%] tw-break-words tw-text-right",
                )
                .find("span")
                .find("span")
                .text.replace("$", "")
            )
            growth_item = item.find(
                "span",
                class_="gecko-up",
            ).text
            dict_popular_crypto[new_item] = (
                new_item,
                price_item,
                "Рост на " + growth_item,
            )
        return dict_popular_crypto
