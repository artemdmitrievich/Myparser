import requests
from bs4 import BeautifulSoup
from time import time, sleep

# from transliterate import translit  # Функция для создания транслита строки
from translit import translit
from langdetect import detect  # Функция для определения языка строки
from headers import Headers
from time import strftime, localtime


# Класс с информацией по конкретной криптовалюте
class Crypto:

    def __init__(self, crypto_name):
        self.__crypto_name = self.__is_valid_crypto_name(crypto_name)
        self.__url_crypto = (
            "https://bitinfocharts.com/ru/" + self.__crypto_name.lower() + "/"
        )
        self.__responce_crypto = requests.get(self.__url_crypto, headers=Headers)
        self.__soup_crypto = BeautifulSoup(self.__responce_crypto.text, "lxml")

    # Проверка валидности полученной при создании экземпляра класса криптовалюте
    # Предварительный транслит криптовалюты если она введена по русски
    # Метод вызывается только внутри класса!!!
    def __is_valid_crypto_name(self, crypto_name):
        if str(detect(crypto_name)) != "fi":
            crypto_name = (
                str(translit(crypto_name))
                .replace("koin", "coin")
                .replace("kesh", "cash")
                .lower()
            )
        else:
            crypto_name = crypto_name.lower()

        is_valid = requests.get(
            "https://bitinfocharts.com/ru/" + crypto_name.lower() + "/", headers=Headers
        ).text
        soup_is_valid = str(BeautifulSoup(is_valid, "lxml").find("h1").text)
        if soup_is_valid == "404 Not Found":
            raise ValueError
        else:
            return crypto_name

    # Получение названия криптовалюты
    @property
    def get_crypto_name(self):
        return self.__crypto_name.lower()

    # Изменение названия криптовалюты
    @get_crypto_name.setter
    def set_crypto_name(self, new_crypto_name):
        self.__crypto_name = self.__is_valid_crypto_name(new_crypto_name)

    # Получение текущей средней стоимости данной криптовалюты
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

        return current_crypto_price, strftime("%H:%M:%S", localtime())

    # Получение капитализации данной криптовалюты
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
        return current_crypto_capitalization, strftime("%H:%M:%S", localtime())


if __name__ == "__main__":
    print(Crypto("bitcoin").get_current_crypto_capitalization())
