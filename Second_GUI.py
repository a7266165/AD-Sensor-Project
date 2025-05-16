import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from widger_helper import button_setup

class SecondWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED測試")
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.ui()

    def ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)


        grid1_box = QtWidgets.QWidget()
        grid1_box.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.grid1_layout = QtWidgets.QGridLayout(grid1_box)

        self.button = button_setup("返回", lambda: None)
        self.button.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.grid1_layout.addWidget(self.button, 0, 0, 1, 2)

        self.main_layout.addWidget(grid1_box)

    def connect_back_button(self, function):
        self.button.clicked.connect(function)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    second_window = SecondWindow()
    second_window.show()
    sys.exit(app.exec())