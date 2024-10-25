# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parser_gui_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 700)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 0")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("QTabBar::tab\n"
"{\n"
"    background: rgb(242, 242, 242);\n"
"    margin-left: 2ex;\n"
"    min-width: 30ex;\n"
"    min-height: 15ex;\n"
"    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    margin-top: 2ex;\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    background: rgb(195, 195, 195);\n"
"}\n"
"\n"
"border: 0\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.menu = QtWidgets.QTabWidget(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(0, 10, 825, 701))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        self.menu.setFont(font)
        self.menu.setStyleSheet("border: 0;")
        self.menu.setTabPosition(QtWidgets.QTabWidget.North)
        self.menu.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.menu.setObjectName("menu")
        self.main_page = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(8)
        self.main_page.setFont(font)
        self.main_page.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.main_page.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.main_page.setAutoFillBackground(False)
        self.main_page.setStyleSheet("background: rgb(195, 195, 195)")
        self.main_page.setObjectName("main_page")
        self.global_capitalization_label = QtWidgets.QLabel(self.main_page)
        self.global_capitalization_label.setGeometry(QtCore.QRect(0, 10, 823, 171))
        self.global_capitalization_label.setStyleSheet("border: 4px solid rgb(148, 148, 148)\n"
"")
        self.global_capitalization_label.setText("")
        self.global_capitalization_label.setObjectName("global_capitalization_label")
        self.global_volume_label = QtWidgets.QLabel(self.main_page)
        self.global_volume_label.setGeometry(QtCore.QRect(0, 191, 823, 171))
        self.global_volume_label.setStyleSheet("border: 4px solid rgb(148, 148, 148)")
        self.global_volume_label.setText("")
        self.global_volume_label.setObjectName("global_volume_label")
        self.capitalization_label = QtWidgets.QLabel(self.main_page)
        self.capitalization_label.setGeometry(QtCore.QRect(4, 14, 401, 163))
        self.capitalization_label.setStyleSheet("border-right: 4px solid rgb(148, 148, 148)")
        self.capitalization_label.setText("")
        self.capitalization_label.setObjectName("capitalization_label")
        self.change_capitalization_label = QtWidgets.QLabel(self.main_page)
        self.change_capitalization_label.setGeometry(QtCore.QRect(405, 14, 414, 163))
        self.change_capitalization_label.setText("")
        self.change_capitalization_label.setObjectName("change_capitalization_label")
        self.volume_label = QtWidgets.QLabel(self.main_page)
        self.volume_label.setGeometry(QtCore.QRect(4, 195, 401, 163))
        self.volume_label.setStyleSheet("border-right: 4px solid rgb(148, 148, 148)")
        self.volume_label.setText("")
        self.volume_label.setObjectName("volume_label")
        self.change_volume_label = QtWidgets.QLabel(self.main_page)
        self.change_volume_label.setGeometry(QtCore.QRect(405, 195, 414, 163))
        self.change_volume_label.setText("")
        self.change_volume_label.setObjectName("change_volume_label")
        self.text_capitalization_label = QtWidgets.QLabel(self.main_page)
        self.text_capitalization_label.setGeometry(QtCore.QRect(30, 30, 341, 21))
        self.text_capitalization_label.setStyleSheet("font-size: 15px")
        self.text_capitalization_label.setObjectName("text_capitalization_label")
        self.result_capitalization_label = QtWidgets.QLabel(self.main_page)
        self.result_capitalization_label.setGeometry(QtCore.QRect(26, 72, 351, 41))
        self.result_capitalization_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 17px;\n"
"font-weight: bold")
        self.result_capitalization_label.setText("")
        self.result_capitalization_label.setObjectName("result_capitalization_label")
        self.change_capitalization_text_label = QtWidgets.QLabel(self.main_page)
        self.change_capitalization_text_label.setGeometry(QtCore.QRect(440, 50, 351, 71))
        self.change_capitalization_text_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 17px;\n"
"font-weight: bold")
        self.change_capitalization_text_label.setText("")
        self.change_capitalization_text_label.setObjectName("change_capitalization_text_label")
        self.text_volume_label = QtWidgets.QLabel(self.main_page)
        self.text_volume_label.setGeometry(QtCore.QRect(30, 210, 341, 21))
        self.text_volume_label.setStyleSheet("font-size: 15px")
        self.text_volume_label.setObjectName("text_volume_label")
        self.result_volume_label = QtWidgets.QLabel(self.main_page)
        self.result_volume_label.setGeometry(QtCore.QRect(26, 250, 351, 41))
        self.result_volume_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 17px;\n"
"font-weight: bold")
        self.result_volume_label.setText("")
        self.result_volume_label.setObjectName("result_volume_label")
        self.change_volume_text_label = QtWidgets.QLabel(self.main_page)
        self.change_volume_text_label.setGeometry(QtCore.QRect(440, 230, 351, 71))
        self.change_volume_text_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 17px;\n"
"font-weight: bold")
        self.change_volume_text_label.setText("")
        self.change_volume_text_label.setObjectName("change_volume_text_label")
        self.menu.addTab(self.main_page, "")
        self.item_page = QtWidgets.QWidget()
        self.item_page.setStyleSheet("background: rgb(195, 195, 195)")
        self.item_page.setObjectName("item_page")
        self.menu.addTab(self.item_page, "")
        self.additional_page = QtWidgets.QWidget()
        self.additional_page.setStyleSheet("background: rgb(195, 195, 195)\n"
"")
        self.additional_page.setObjectName("additional_page")
        self.menu.addTab(self.additional_page, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.menu.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.text_capitalization_label.setText(_translate("MainWindow", "Общая рыночная капитализация криптовалюты:"))
        self.text_volume_label.setText(_translate("MainWindow", "Общая рыночная капитализация криптовалюты:"))
        self.menu.setTabText(self.menu.indexOf(self.main_page), _translate("MainWindow", "Main"))
        self.menu.setTabText(self.menu.indexOf(self.item_page), _translate("MainWindow", "Item"))
        self.menu.setTabText(self.menu.indexOf(self.additional_page), _translate("MainWindow", "Additional"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
