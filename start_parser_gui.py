import webbrowser, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from Main_info_crypto_parser import General, Additional_CoinGecko_info
from parser_gui import Ui_MainWindow
from time import sleep, time
from PyQt5.QtCore import Qt

# "icons/icons8-телеграм-96.png" - путь к иконке телеграма


class My_Ui_MainWindow(Ui_MainWindow):

    def __init__(self, MainWindow):
        # Создание фиксированного размера окна
        MainWindow.setFixedSize(823, 700)
        # Полное наследование от Ui_MainWindow
        super().setupUi(MainWindow)

        # Создание иконок trending_up и trending_down
        self.Icon_trending_up = QtGui.QIcon()
        self.Icon_trending_down = QtGui.QIcon()
        self.Icon_trending_up.addPixmap(
            QtGui.QPixmap("icons/trending_up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Icon_trending_down.addPixmap(
            QtGui.QPixmap("icons/trending_down.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )

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

        # Создание ссылки на донаты автору
        donates_url = "https://www.coingecko.com/ru"  # url на донаты автору
        self.Switch_to_support_the_autor_Button.clicked.connect(
            lambda: webbrowser.open(donates_url)
        )

        # Обработка кнопок обновления страницы
        self.Update_Main_Button.clicked.connect(self._Update_main_page)
        self.Update_Additional_Button.clicked.connect(self._Update_additional_page)

        # Сразу при инициализации обновляем main и additional page
        self._Update_main_page()
        self._Update_additional_page()

    # Функция обновления страницы additional
    def _Update_additional_page(self):
        Current_additional = Additional_CoinGecko_info()

        # Обновление таблицы криптовалют, с наибольшим ростом
        Current_greatest_growth_crypto = Current_additional.get_greatest_growth_crypto()
        # Обновление названий
        if len(Current_greatest_growth_crypto[0][0][0]) > 18:
            self.Max_growth_name_label_1.setText(
                Current_greatest_growth_crypto[0][0][0][0:15] + "..."
            )
        else:
            self.Max_growth_name_label_1.setText(
                " " * ((18 - len(Current_greatest_growth_crypto[0][0][0])) // 2)
                + Current_greatest_growth_crypto[0][0][0]
            )
        if len(Current_greatest_growth_crypto[0][1][0]) > 18:
            self.Max_growth_name_label_2.setText(
                Current_greatest_growth_crypto[0][1][0][0:15] + "..."
            )
        else:
            self.Max_growth_name_label_2.setText(
                " " * ((18 - len(Current_greatest_growth_crypto[0][0][0])) // 2)
                + Current_greatest_growth_crypto[0][1][0]
            )
        if len(Current_greatest_growth_crypto[0][2][0]) > 18:
            self.Max_growth_name_label_3.setText(
                Current_greatest_growth_crypto[0][2][0][0:15] + "..."
            )
        else:
            self.Max_growth_name_label_3.setText(
                " " * ((18 - len(Current_greatest_growth_crypto[0][0][0])) // 2)
                + Current_greatest_growth_crypto[0][2][0]
            )
        # Обновление времени
        self.Max_growth_time_label_1.setText(
            " " * 12 + Current_greatest_growth_crypto[1]
        )
        self.Max_growth_time_label_2.setText(
            " " * 12 + Current_greatest_growth_crypto[1]
        )
        self.Max_growth_time_label_3.setText(
            " " * 12 + Current_greatest_growth_crypto[1]
        )
        # Обновление стоимости
        self.Max_growth_cost_label_1.setText(
            " " * 8 + "$ " + Current_greatest_growth_crypto[0][0][1]
        )
        self.Max_growth_cost_label_2.setText(
            " " * 8 + "$ " + Current_greatest_growth_crypto[0][1][1]
        )
        self.Max_growth_cost_label_3.setText(
            " " * 8 + "$ " + Current_greatest_growth_crypto[0][2][1]
        )
        # Обновление увеличения
        self.Max_growth_change_label_1.setText(
            " " * 7 + Current_greatest_growth_crypto[0][0][2]
        )
        self.Max_growth_change_label_2.setText(
            " " * 7 + Current_greatest_growth_crypto[0][1][2]
        )
        self.Max_growth_change_label_3.setText(
            " " * 7 + Current_greatest_growth_crypto[0][2][2]
        )

        # Обновление таблицы самых популярных криптовалют
        Current_popular_crypto = Current_additional.get_popular_crypto()
        # Обновление названий
        if len(Current_popular_crypto[0][0][0]) > 18:
            self.Popular_name_label_1.setText(
                Current_popular_crypto[0][0][0][0:15] + "..."
            )
        else:
            self.Popular_name_label_1.setText(
                " " * ((18 - len(Current_popular_crypto[0][0][0])) // 2)
                + Current_popular_crypto[0][0][0]
            )
        if len(Current_popular_crypto[0][1][0]) > 18:
            self.Max_growth_name_label_2.setText(
                Current_popular_crypto[0][1][0][0:15] + "..."
            )
        else:
            self.Popular_name_label_2.setText(
                " " * ((18 - len(Current_popular_crypto[0][0][0])) // 2)
                + Current_popular_crypto[0][1][0]
            )
        if len(Current_popular_crypto[0][2][0]) > 18:
            self.Popular_name_label_3.setText(
                Current_popular_crypto[0][2][0][0:15] + "..."
            )
        else:
            self.Popular_name_label_3.setText(
                " " * ((18 - len(Current_popular_crypto[0][0][0])) // 2)
                + Current_popular_crypto[0][2][0]
            )
        # Обновление времени
        self.Popular_time_label_1.setText(" " * 12 + Current_popular_crypto[1])
        self.Popular_time_label_2.setText(" " * 12 + Current_popular_crypto[1])
        self.Popular_time_label_3.setText(" " * 12 + Current_popular_crypto[1])
        # Обновление стоимости
        self.Popular_cost_label_1.setText(
            " " * 8 + "$ " + Current_popular_crypto[0][0][1]
        )
        self.Popular_cost_label_2.setText(
            " " * 8 + "$ " + Current_popular_crypto[0][1][1]
        )
        self.Popular_cost_label_3.setText(
            " " * 8 + "$ " + Current_popular_crypto[0][2][1]
        )
        # Обновление значений изменения стоимости
        self.Popular_change_label_1.setText(" " * 7 + Current_popular_crypto[0][0][2])
        self.Popular_change_label_2.setText(" " * 7 + Current_popular_crypto[0][1][2])
        self.Popular_change_label_3.setText(" " * 7 + Current_popular_crypto[0][2][2])
        # Вызов функции для обновления иконок и стилей у самых популярных криптовалют
        self.__Create_Icon_and_Style(Current_popular_crypto)

    # Обновляет иконки и стили у самых популярных криптовалют
    def __Create_Icon_and_Style(self, Current_popular_crypto):
        if Current_popular_crypto[0][0][3] == "down":
            self.Popular_change_label_1.setStyleSheet(
                "color: rgb(255,0,0);\n"
                "font-size: 16px;\n"
                "font-weight: bold;\n"
                "background-color: rgb(157, 0, 255);"
            )
            self.Popular_Icon_Button_1.setIcon(self.Icon_trending_down)
        if Current_popular_crypto[0][1][3] == "down":
            self.Popular_change_label_2.setStyleSheet(
                "color: rgb(255,0,0);\n"
                "font-size: 16px;\n"
                "font-weight: bold;\n"
                "background-color: rgb(157, 0, 255);"
            )
            self.Popular_Icon_Button_2.setIcon(self.Icon_trending_down)
        if Current_popular_crypto[0][2][3] == "down":
            self.Popular_change_label_3.setStyleSheet(
                "color: rgb(255,0,0);\n"
                "font-size: 16px;\n"
                "font-weight: bold;\n"
                "background-color: rgb(157, 0, 255);"
            )
            self.Popular_Icon_Button_3.setIcon(self.Icon_trending_down)

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

    # Обновляет все страницы
    def _Update_all(self):
        self._Update_additional_page()
        self._Update_main_page()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = My_Ui_MainWindow(MainWindow=MainWindow)
    # Создание цикла обновлений главной страницы
    timer = QtCore.QTimer()
    timer.timeout.connect(ui._Update_all)
    timer.start(300000)
    MainWindow.show()
    sys.exit(app.exec_())
