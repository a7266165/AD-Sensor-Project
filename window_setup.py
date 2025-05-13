from PyQt6 import QtWidgets
import sys

def window_setup(Form, title, background_color_RGB):
    # 設定視窗標題
    Form.setWindowTitle(title)
    #  設定視窗顏色
    r, g, b = background_color_RGB
    Form.setStyleSheet(f'background-color: rgb({r}, {g}, {b});')


def window_size(Form, app, window_size):
    # 設定視窗大小
    width, height = window_size
    Form.setFixedSize(width, height)
    window_width = Form.width()
    window_height = Form.height()

    # 取得螢幕解析度
    screen = app.primaryScreen()
    screen_width = screen.size().width()
    screen_height = screen.size().height()

    # 設定視窗位置(置中)
    window_x = int((screen_width - window_width) / 2)
    window_y = int((screen_height - window_height) / 2 - 50)
    Form.move(window_x, window_y)  # 設定視窗位置


def __main__():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    window_setup(Form, "Window_setup", (255, 255, 255))
    window_size(Form, app, window_size = (800, 450))
    Form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    __main__()
