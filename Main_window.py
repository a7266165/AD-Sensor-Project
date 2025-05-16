# from test import SecondWindow, ThirdWindow, FourthWindow, MainWindow
from Firtst_GUI import FirstWindow
from Second_GUI import SecondWindow
from PyQt6 import QtWidgets, QtGui, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = FirstWindow()
        self.window1.connect_next_button(self.show_second_window)
        self.window2 = SecondWindow()
        self.window2.connect_back_button(self.show_first_window)

    def show(self): # 程式開始時顯示第一個視窗
        self.window1.show()
    
    def show_second_window(self):
        self.window1.hide()
        self.window2.show()

    def show_first_window(self):
        self.window2.hide()
        self.window1.show()





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    

    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())