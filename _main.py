from _1_Personal_GUI import InfoWindow
from _2_Photography_window import CapWindow
from PyQt6 import QtWidgets
import sys


# from LED_GUI import LEDWindow, LEDPresenter
class ADRecordingAnalysisWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.info_window = InfoWindow()
        self.info_window.next_button(self.capture_pics)
        self.capture_window = CapWindow()

    # 初始窗口
    def init(self):
        self.info_window.setFixedSize(600, 1000)
        self.capture_window.setFixedSize(600, 1000)
        self.info_window.show()

    def capture_pics(self):
        self.info_window.hide()
        self.capture_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ADRecordingAnalysisWindow()
    window.init()
    sys.exit(app.exec())
