from Main_info_crypto_parser import General
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import webbrowser


class Main_page:

    def __init__(self):
        # Создание ссылки на coingecko.com
        self.Value_information_source_label.setText(
            '<a href="https://www.coingecko.com/ru">coingecko.com</a>'
        )
        self.Value_information_source_label.setTextFormat(Qt.RichText)
        self.Value_information_source_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction
        )
        self.Value_information_source_label.setOpenExternalLinks(True)

        # Создание ссылки на телеграм-бота
        telegram_bot_url = "https://www.coingecko.com/ru"  # url телеграм-бота
        self.Switch_to_telegram_bot_Button.clicked.connect(
            lambda: webbrowser.open(telegram_bot_url)
        )
        self.Telegram_Icon_Button.clicked.connect(
            lambda: webbrowser.open(telegram_bot_url)
        )

        # Создание ссылки на донаты автору
        donates_url = "https://www.coingecko.com/ru"  # url на донаты автору
        self.Switch_to_support_the_autor_Button.clicked.connect(
            lambda: webbrowser.open(donates_url)
        )
        self.Coin_Icon_Button.clicked.connect(lambda: webbrowser.open(donates_url))

    # Обработка нажатия кнопки "Нажмите, чтобы обновить" на главной странице
    # Срабатывает в промежутке времени от 5 до 8 секунд
    def _Update_main_page(self):

        # Создание текущего экземпляра класса и вызов функций
        Current_General = General()
        Current_data_market_capitalization = (
            Current_General.get_data_market_capitalization()
        )
        Current_change_market_capitalization = (
            Current_General.get_change_market_capitalization()
        )
        Current_total_trading_volume_per_day = (
            Current_General.get_total_trading_volume_per_day()
        )

        # Проверка направления изменения рыночной капитализации
        # и установка нужной иконки тренда
        if Current_change_market_capitalization[2] == "up":
            self.Direction_change_capitalization_Icon_Button.setIcon(
                self.Icon_trending_up
            )
            self.Direction_change_capitalization_Icon_Button.setIconSize(
                QtCore.QSize(40, 40)
            )
        else:
            self.Direction_change_capitalization_Icon_Button.setIcon(
                self.Icon_trending_down
            )
            self.Direction_change_capitalization_Icon_Button.setIconSize(
                QtCore.QSize(40, 40)
            )

        # Установка основныз значений
        self.Value_capitalization_label.setText(
            f"$ {Current_data_market_capitalization[0]}"
        )
        self.Time_update_capitalization_label.setText(
            f"Обновлено в {Current_data_market_capitalization[1]}"
        )
        self.Value_volume_label.setText(f"$ {Current_total_trading_volume_per_day[0]}")
        self.Time_update_volume_label.setText(
            f"Обновлено в {Current_total_trading_volume_per_day[1]}"
        )
        self.Value_change_capitalization_label.setText(
            self.__Create_output_to_value_change_capitalization_label(
                Current_change_market_capitalization
            )
        )
        self.Time_update_change_capitalization_label.setText(
            f"Обновлено в {Current_change_market_capitalization[1]}"
        )

    # Создание текста для обновления изменения рыночной капитализации
    def __Create_output_to_value_change_capitalization_label(self, Current):
        if Current[2] == "down":
            direction = "Понизилась на"
        else:
            direction = "Повысилась на"
            self.Value_change_capitalization_label.setStyleSheet(
                "font-size: 16px;\n"
                "color: rgb(0,255,0);\n"
                "background: rgba(255,255,255,0);\n"
                "font-weight: bold"
            )
        return f"{direction} {Current[0]}"
