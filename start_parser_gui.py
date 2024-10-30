import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from parser_gui import Ui_MainWindow
from Additional_page import Additional_page
from Main_page import Main_page

# "icons/icons8-телеграм-96.png" - путь к иконке телеграма


class My_Ui_MainWindow(Ui_MainWindow, Additional_page, Main_page):

    def __init__(self, MainWindow):
        # Создание фиксированного размера окна
        MainWindow.setFixedSize(823, 700)
        # Полное наследование от Ui_MainWindow, Main_page
        super().setupUi(MainWindow)
        super(Main_page, self).__init__()

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

        # Обработка кнопок обновления страницы
        self.Update_Main_Button.clicked.connect(self._Update_main_page)
        self.Update_Additional_Button.clicked.connect(self._Update_additional_page)

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
