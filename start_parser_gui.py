from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from Main_info_crypto_parser import General
from parser_gui import Ui_MainWindow
from time import sleep

class My_Ui_MainWindow(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().setupUi(MainWindow)
        self.price = General.get_data_market_capitalization() + "$"
        self.result_capitalization_label.setText(self.price)
        self.result_volume_label.setText("asdfasdf")
        
    # def auto_get_data_market_capitalization(self):
    #     self.price += '1'
    #     self.result_capitalization_label.setText(self.price)
    #     print("asdf")
    #     return self.price

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = My_Ui_MainWindow(MainWindow=MainWindow)
    # QTimer.singleShot(200, My_Ui_MainWindow(MainWindow=MainWindow).auto_get_data_market_capitalization)
    MainWindow.show()
    sys.exit(app.exec_())