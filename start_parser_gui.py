from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from Main_info_crypto_parser import General
from parser_gui import Ui_MainWindow
from time import sleep, time


class My_Ui_MainWindow(Ui_MainWindow):

    def __init__(self, MainWindow):
        super().setupUi(MainWindow)
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

    # Обработка нажатия кнопки "Нажмите, чтобы обновить" на главной странице
    # Срабатывает в промежутке времени от 5 до 8 секунд
    def _Update_main_page(self):
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

    #Создание текста для обновления изменения рыночной капитализации
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
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = My_Ui_MainWindow(MainWindow=MainWindow)
    timer = QtCore.QTimer()
    timer.timeout.connect(ui._Update_main_page)
    timer.start(4000)
    MainWindow.show()
    sys.exit(app.exec_())
