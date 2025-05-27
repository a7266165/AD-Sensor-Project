from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import cv2
from _cap_pics import CameraDevice

class CapWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拍攝視窗")
        self.resize(1024, 768)
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.is_recording = False
        
        # 設定根佈局 (layer 0)
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)
        
        # ===== 第一母區塊 - title =====#
        # 創建 & 設定標題區塊(layer 1)
        title_parent_widget = QtWidgets.QWidget()
        title_parent_widget.setStyleSheet("")
        title_parent_widget_layout = QtWidgets.QHBoxLayout(title_parent_widget)

        # 創建 & 設定標題內容(layer 2)
        title_content = QtWidgets.QLabel("Camera")
        title_content.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(0, 0, 0); border: 0px;")
        title_content.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # 將標題內容(layer 2)添加到標題區塊(layer 1)
        title_parent_widget_layout.addWidget(title_content)

        # 將標題區塊(layer 1)添加到主佈局(layer 0)
        root_layout.addWidget(title_parent_widget)
        # ===== 第一母區塊 - title =====#
        
        # ===== 第二母區塊 - camera =====#
        # 創建 & 設定相機畫面背景 (layer 1)
        camera_frame = QtWidgets.QFrame()
        camera_frame.setStyleSheet("background-color: #333333; border-radius: 8px;")
        camera_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        camera_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        camera_layout = QtWidgets.QVBoxLayout(camera_frame)
        camera_layout.setContentsMargins(10, 10, 10, 10)
        
        # 創建 & 設定相機畫面區塊 (layer 2)
        cap_pic_region = QtWidgets.QLabel()
        cap_pic_region.setStyleSheet("background-color: black; border-radius: 4px;")
        cap_pic_region.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        cap_pic_region.setMinimumHeight(500)

        # 將相機畫面區塊(layer 2)添加到相機畫面背景 (layer 1)
        camera_layout.addWidget(cap_pic_region)
        
        # 將相機畫面區塊(layer 1)添加到主佈局(layer 0)
        root_layout.addWidget(camera_frame)
        # ===== 第二母區塊 - camera =====#

        # ===== 第三母區塊 - control buttons =====#
        # 創建 & 設定按鈕區塊 (layer 1)
        button_frame = QtWidgets.QFrame()
        button_frame.setStyleSheet("background-color: #e0e0e0; border-radius: 8px;")
        button_layout = QtWidgets.QHBoxLayout(button_frame)
        button_layout.setContentsMargins(20, 15, 20, 15)
        button_layout.setSpacing(15)
        
        button_style = """
            QPushButton {
                background-color: #d54e4e;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #888888;
            }
        """
        
        # 創建 & 設定拍攝按鈕 (layer 2)
        record_button = QtWidgets.QPushButton("Start Recording")
        record_button.setStyleSheet(button_style)

        # 將拍攝按鈕 (layer 2) 添加到按鈕區塊 (layer 1)
        button_layout.addWidget(record_button)
        
        # 將按鈕區塊(layer 1)添加到主佈局(layer 0)
        root_layout.addWidget(button_frame)
        # ===== 第三母區塊 - control buttons ===== #

        # 建立相機物件
        camera = CameraDevice(camera_type="RealSense")

        # 巢狀函式 - 顯示相機畫面
        def show_frame():
            frame = camera.get_frame()
            if frame is None:
                return

            h, w, ch = frame.shape
            bytes_per_line = ch * w

            q_img = QtGui.QImage(
                frame.data, w, h, bytes_per_line,
                QtGui.QImage.Format.Format_BGR888
            )

            cap_pic_region.setPixmap(QtGui.QPixmap.fromImage(q_img))

        # 用 QTimer 定時呼叫巢狀函式
        timer = QtCore.QTimer(self)  
        timer.timeout.connect(show_frame)
        timer.start(30)  # 多久呼叫一次（毫秒）

    def get_frame(self):
        """獲取畫面"""

        frame = 

        return self.camera.get_frame()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    win = CapWindow()
    win.show()
    sys.exit(app.exec())