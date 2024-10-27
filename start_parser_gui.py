import webbrowser, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from Main_info_crypto_parser import General
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

        # Заполнение значений в основных окнах
        self.Value_capitalization_label.setText(
            f"{General.get_data_market_capitalization()[0]}$"
        )
        self.Time_update_capitalization_label.setText(
            f"Обновлено в {General.get_data_market_capitalization()[1]}"
        )
        self.Value_volume_label.setText(
            f"{General.get_total_trading_volume_per_day()[0]}$"
        )
        self.Time_update_volume_label.setText(
            f"Обновлено в {General.get_total_trading_volume_per_day()[1]}"
        )
        self.Value_change_capitalization_label.setText(
            self.__Create_output_to_value_change_capitalization_label()
        )
        self.Time_update_change_capitalization_label.setText(
            f"Обновлено в {General.get_change_market_capitalization()[1]}"
        )
        self.Update_Button.clicked.connect(self._Update_main_page)

        # Создание ссылки на coingecko.com
        self.Value_information_source_label.setText(
            '<a href="https://www.coingecko.com/ru">coingecko.com</a>'
        )
        self.Value_information_source_label.setTextFormat(Qt.RichText)
        self.Value_information_source_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction
        )
        self.Value_information_source_label.setOpenExternalLinks(True)

        # Создание ссылок на телеграм-бота
        telegram_bot_url = "https://www.coingecko.com/ru"  # url телеграм-бота
        self.Telegram_Icon_Button.clicked.connect(
            lambda: webbrowser.open(telegram_bot_url)
        )
        self.Telegram_link_Button.clicked.connect(
            lambda: webbrowser.open(telegram_bot_url)
        )

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
        # Проверка направления изменения рыночной капитализации
        # и установка нужной иконки тренда
        if General.get_change_market_capitalization()[2] == "up":
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

    # Обработка нажатия кнопки "Нажмите, чтобы обновить" на главной странице
    # Срабатывает в промежутке времени от 5 до 8 секунд
    def _Update_main_page(self):
        # lambda: self.start_animation()
        self.Value_capitalization_label.setText(
            f"{General.get_data_market_capitalization()[0]}$"
        )
        self.Time_update_capitalization_label.setText(
            f"Обновлено в {General.get_data_market_capitalization()[1]}"
        )
        self.Value_volume_label.setText(
            f"{General.get_total_trading_volume_per_day()[0]}$"
        )
        self.Time_update_volume_label.setText(
            f"Обновлено в {General.get_total_trading_volume_per_day()[1]}"
        )
        self.Value_change_capitalization_label.setText(
            self.__Create_output_to_value_change_capitalization_label()
        )
        self.Time_update_change_capitalization_label.setText(
            f"Обновлено в {General.get_change_market_capitalization()[1]}"
        )

    # Создание текста для обновления изменения рыночной капитализации
    def __Create_output_to_value_change_capitalization_label(self):
        if General.get_change_market_capitalization()[2] == "down":
            direction = "Понизилась на"
        else:
            direction = "Повысилась на"
            self.Value_change_capitalization_label.setStyleSheet(
                "font-size: 16px;\n"
                "color: rgb(0,255,0);\n"
                "background: rgba(255,255,255,0);\n"
                "font-weight: bold"
            )
        return f"{direction} {General.get_change_market_capitalization()[0]}"


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = My_Ui_MainWindow(MainWindow=MainWindow)
    # Создание цикла обновлений главной страницы
    timer = QtCore.QTimer()
    timer.timeout.connect(ui._Update_main_page)
    timer.start(300000)
    MainWindow.show()
    sys.exit(app.exec_())
