from time import strftime, localtime
from static.Soup_main_CoinGecko import coingecko_soup


# Класс с общей информацией по криптовалюте
class General:
    def __init__(self):
        pass

    # Получение общей капитализации криптовалюты
    def get_data_market_capitalization(self):
        data_market_capitalization = (
            coingecko_soup()
            .find(
                "div",
                class_="tw-font-bold tw-text-gray-900 dark:tw-text-moon-50 tw-text-lg tw-leading-7",
            )
            .text.replace("\n", "")
            .replace("$", "")
        )
        return data_market_capitalization, strftime("%H:%M:%S", localtime())

    # Получение изменения общей капитализации криптовалюты за 24 часа
    def get_change_market_capitalization(self):
        capitalization_div = coingecko_soup().find(
            "div",
            class_="tw-mt-1 tw-flex tw-flex-wrap tw-items-center tw-text-gray-500 dark:tw-text-moon-200 tw-font-semibold tw-text-sm tw-leading-5",
        )
        change_market_capitalization_value = 0
        if "gecko-down" in str(capitalization_div):
            direction = "down"
            change_market_capitalization_value = capitalization_div.find(
                "span", class_="gecko-down"
            ).text
        else:
            direction = "up"
            change_market_capitalization_value = capitalization_div.find(
                "span", class_="gecko-up"
            ).text
        return (
            change_market_capitalization_value,
            strftime("%H:%M:%S", localtime()),
            direction,
        )

    # Получение общего объёма торгов за 24 часа
    def get_total_trading_volume_per_day(self):
        total_trading_volume_per_day = (
            coingecko_soup()
            .find(
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
        return total_trading_volume_per_day, strftime("%H:%M:%S", localtime())


# Класс с дополнительной информацией по криптовалюте
class Additional_CoinGecko_info:

    def __init__(self):
        self.general_divs = coingecko_soup().find_all(
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
        for number in range(3):
            item = class_popular_crypto[number]
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
            if "gecko-down" in str(item):
                direction = "down"
                change_value = item.find(
                    "span",
                    class_="gecko-down",
                ).text
            elif "gecko-up" in str(item):
                direction = "up"
                change_value = item.find(
                    "span",
                    class_="gecko-up",
                ).text
            else:
                direction = "None"
                change_value = "None"
            dict_popular_crypto[number] = name_item, price_item, change_value, direction
        return dict_popular_crypto, strftime("%H:%M:%S", localtime())

    # Получение информации по 3 криптовалютам с самым большим ростом за последние 24 часа по версии CoinGecko.com
    def get_greatest_growth_crypto(self):
        class_greatest_growth_crypto = self.general_divs[1].find_all(
            "div",
            class_="tw-flex tw-justify-between tw-px-2 tw-py-2.5 hover:tw-bg-gray-50 tw-rounded-lg dark:hover:tw-bg-moon-700",
        )
        dict_greatest_growth_crypto = {}
        for number in range(3):
            item = class_greatest_growth_crypto[number]
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
            growth_item = item.find(
                "span",
                class_="gecko-up",
            ).text
            dict_greatest_growth_crypto[number] = (
                name_item,
                price_item,
                growth_item,
            )
        return dict_greatest_growth_crypto, strftime("%H:%M:%S", localtime())
