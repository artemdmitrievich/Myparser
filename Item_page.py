from Item_info_crypto_parser import Crypto
# from transliterate import translit  # Функция для создания транслита строки
from translit import translit
from langdetect import detect  # Функция для определения языка строки
import requests
from bs4 import BeautifulSoup
from static.headers import Headers


class Item_page:

    # Обновление страницы Item
    def _Update_Item_page(self):
        crypto_name = str(self.Input_item_lineEdit.text())
        if crypto_name != "":
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
                "https://bitinfocharts.com/ru/" + crypto_name.lower() + "/",
                headers=Headers,
            ).text
            soup_is_valid = str(BeautifulSoup(is_valid, "lxml").find("h1").text)
            if soup_is_valid == "404 Not Found":
                self.Text_item_capitalization_label.setText("")
                self.Time_update_item_capitalization_label.setText("")
                self.Text_avarage_item_price_label.setText("")
                self.Value_change_avarage_item_price_label.setText("")
                self.Time_update_avarage_item_price_label.setText("")
                self.Value_item_capitalization_label.setText(
                    "Введённая криптовалюта\nне найдена!!!"
                )
                self.Value_item_capitalization_label.setStyleSheet(
                    "font-size: 22px;\n"
                    "color: rgb(255,0,0);\n"
                    "background: rgba(255,255,255,0);\n"
                )

            else:
                self.Value_item_capitalization_label.setStyleSheet(
                    "font-size: 16px;\n"
                    "color: rgb(0,255,0);\n"
                    "background: rgba(255,255,255,0);\n"
                    "font-weight: bold"
                )
                Current_crypto = Crypto(self.Input_item_lineEdit.text())
                Current_crypto_name = Current_crypto.get_crypto_name
                Current_crypto_capitalization = (
                    Current_crypto.get_current_crypto_capitalization()
                )
                Current_crypto_avarage_price = (
                    Current_crypto.get_current_average_crypto_price()
                )
                if Current_crypto_capitalization[0] != "Нет информации":
                    self.Value_item_capitalization_label.setText(
                        f"$ {Current_crypto_capitalization[0]}"
                    )
                else:
                    self.Value_item_capitalization_label.setText(
                        f"{Current_crypto_capitalization[0]}"
                    )
                self.Text_item_capitalization_label.setText(
                    f"Рыночная капитализация {Current_crypto_name}:"
                )
                self.Time_update_item_capitalization_label.setText(
                    f"Обновлено в {Current_crypto_capitalization[1]}"
                )
                self.Value_change_avarage_item_price_label.setText(
                    f"$ {Current_crypto_avarage_price[0]}"
                )
                self.Text_avarage_item_price_label.setText(
                    f"Средняя стоимость {Current_crypto_name}:"
                )
                self.Time_update_avarage_item_price_label.setText(
                    f"Обновлено в {Current_crypto_avarage_price[1]}"
                )
                self.Input_item_lineEdit.clear()

        else:
            if self.Text_item_capitalization_label.text() != "":
                Current_crypto = Crypto(
                    self.Text_item_capitalization_label.text()
                    .replace("Рыночная капитализация ", "")
                    .replace(":", "")
                )
                Current_crypto_name = Current_crypto.get_crypto_name
                Current_crypto_capitalization = (
                    Current_crypto.get_current_crypto_capitalization()
                )
                Current_crypto_avarage_price = (
                    Current_crypto.get_current_average_crypto_price()
                )
                if Current_crypto_capitalization[0] != "Нет информации":
                    self.Value_item_capitalization_label.setText(
                        f"$ {Current_crypto_capitalization[0]}"
                    )
                else:
                    self.Value_item_capitalization_label.setText(
                        f"{Current_crypto_capitalization[0]}"
                    )
                self.Text_item_capitalization_label.setText(
                    f"Рыночная капитализация {Current_crypto_name}:"
                )
                self.Time_update_item_capitalization_label.setText(
                    f"Обновлено в {Current_crypto_capitalization[1]}"
                )
                self.Value_change_avarage_item_price_label.setText(
                    f"$ {Current_crypto_avarage_price[0]}"
                )
                self.Text_avarage_item_price_label.setText(
                    f"Средняя стоимость {Current_crypto_name}"
                )
                self.Time_update_avarage_item_price_label.setText(
                    f"Обновлено в {Current_crypto_avarage_price[1]}"
                )
