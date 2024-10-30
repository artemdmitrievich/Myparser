import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from parser_gui import Ui_MainWindow
from Additional_page import Additional_page
from Main_page import Main_page
from Item_page import Item_page
from Item_info_crypto_parser import Crypto
from PyQt5.QtCore import Qt
import webbrowser
import res_rc

# "icons/icons8-телеграм-96.png" - путь к иконке телеграма


class My_Ui_MainWindow(Ui_MainWindow, Additional_page, Main_page, Item_page):

    def __init__(self, MainWindow):
        # Создание фиксированного размера окна
        MainWindow.setFixedSize(823, 700)
        # Полное наследование от Ui_MainWindow, Main_page, Item_page
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle("My_crypto_info_portal")
        MainWindow.setWindowIcon(QtGui.QIcon(":/icons/icons/coin.png"))

        # Создание иконок trending_up и trending_down
        self.Icon_trending_up = QtGui.QIcon()
        self.Icon_trending_down = QtGui.QIcon()
        self.Icon_trending_up.addPixmap(
            QtGui.QPixmap(":/icons/icons/trending_up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Icon_trending_down.addPixmap(
            QtGui.QPixmap(":/icons/icons/trending_down.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )

        # Создание ссылки на телеграм-бота
        telegram_bot_url = "https://www.coingecko.com/ru"  # url телеграм-бота
        self.Switch_to_telegram_bot_Button_2.clicked.connect(
            lambda: webbrowser.open(telegram_bot_url)
        )
        self.Telegram_Icon_Button_2.clicked.connect(
            lambda: webbrowser.open(telegram_bot_url)
        )

        # Создание ссылки на донаты автору
        donates_url = "https://www.coingecko.com/ru"  # url на донаты автору
        self.Switch_to_support_the_autor_Button_2.clicked.connect(
            lambda: webbrowser.open(donates_url)
        )
        self.Coin_Icon_Button_2.clicked.connect(lambda: webbrowser.open(donates_url))

        Current_crypto = Crypto("bitcoin")
        Current_crypto_name = Current_crypto.get_crypto_name
        Current_crypto_capitalization = (
            Current_crypto.get_current_crypto_capitalization()
        )
        Current_crypto_avarage_price = Current_crypto.get_current_average_crypto_price()
        self.Value_item_capitalization_label.setText(
            f"$ {Current_crypto_capitalization[0]}"
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

        self.Value_information_source_label_2.setText(
            '<a href="https://bitinfocharts.com/ru/">bitinfocharts.com</a>'
        )
        self.Value_information_source_label_2.setTextFormat(Qt.RichText)
        self.Value_information_source_label_2.setTextInteractionFlags(
            Qt.TextBrowserInteraction
        )
        self.Value_information_source_label_2.setOpenExternalLinks(True)

        # Обработка кнопок обновления страницы
        self.Update_Main_Button.clicked.connect(self._Update_main_page)
        self.Update_Additional_Button.clicked.connect(self._Update_additional_page)
        self.Update_item_Button.clicked.connect(self._Update_Item_page)

        # Обработка кнопки сохранить Item_page
        self.Get_input_Button.clicked.connect(self._Update_Item_page)

        # Сразу при инициализации обновляем main и additional page
        self._Update_main_page()
        self._Update_additional_page()

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
