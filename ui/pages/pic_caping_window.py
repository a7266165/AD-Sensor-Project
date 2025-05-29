# 測試用 - 把母資料夾路徑加入系統路徑
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)


# pic_caping_window.py - 重構後的拍攝視窗

import cv2
import sys
import os
import datetime
from PyQt6 import QtWidgets, QtCore, QtGui

# 導入樣式設定
from ui.styles.pic_caping_window_style import (
    MAIN_WINDOW_STYLE,
    TITLE_STYLE,
    CAMERA_REGION_STYLE,
    BUTTON_STYLE,
    COUNTDOWN_LABEL_STYLE,
    PATH_LABEL_STYLE,
)

# 導入工具模組
from utils.cap_pic import RealSenseCamera, get_frames
from utils.led_controller import LEDController, LEDWorker, find_arduino_port


class PicCapingWindow(QtWidgets.QFrame):
    """拍攝視窗主類別"""

    analysis_requested = QtCore.pyqtSignal()  # 即時分析請求信號

    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_parameters()
        self._init_led_controller()
        self._init_camera()
        self._init_ui()
        self._init_timers()

    def _init_window(self):
        """初始化視窗設定"""
        self.setWindowTitle("拍攝視窗")
        self.resize(1024, 768)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def _init_parameters(self):
        """初始化參數"""
        self.save_folder = None
        self.is_recording = False
        self.record_duration = 40  # 總錄製秒數

    def _init_led_controller(self):
        """初始化LED控制器"""
        arduino_port = find_arduino_port()
        self.led_ctrl = LEDController(arduino_port) if arduino_port else None
        if not self.led_ctrl:
            print("警告：未偵測到 Arduino，LED 功能將無法使用。")

    def _init_camera(self):
        """初始化相機與臉部偵測"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.cam = RealSenseCamera(width=848, height=480, fps=60)
        self.cam.start()

    def _init_ui(self):
        """初始化使用者介面"""
        # 根佈局 layer 0
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)

        # 標題 layer 1
        self._create_title(root_layout)

        # 顯示畫面 layer 1
        self._create_camera_region(root_layout)

        # 控制按鈕 layer 1
        self._create_control_buttons(root_layout)

        # 倒數計時 layer 1
        self._create_countdown_label(root_layout)

        # 路徑顯示 layer 1
        self._create_path_label(root_layout)

    def _create_title(self, layout):
        """創建標題"""
        title = QtWidgets.QLabel("Camera")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

    def _create_camera_region(self, layout):
        """創建攝像頭顯示區域"""
        self.cap_pic_region = QtWidgets.QLabel()
        self.cap_pic_region.setStyleSheet(CAMERA_REGION_STYLE)
        self.cap_pic_region.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cap_pic_region.setMinimumHeight(500)
        layout.addWidget(self.cap_pic_region)

    def _create_control_buttons(self, layout):
        """創建控制按鈕區域"""
        control_widget = QtWidgets.QWidget()
        control_layout = QtWidgets.QHBoxLayout(control_widget)
        control_layout.setSpacing(15)

        # 錄製按鈕 layer 2
        self.record_button = QtWidgets.QPushButton("Start Recording")
        self.record_button.setStyleSheet(BUTTON_STYLE)
        self.record_button.clicked.connect(self.on_record_button)
        control_layout.addWidget(self.record_button)

        # 分析按鈕 layer 2
        self.analysis_button = QtWidgets.QPushButton("即時分析")
        self.analysis_button.setStyleSheet(BUTTON_STYLE)
        self.analysis_button.hide()
        self.analysis_button.clicked.connect(self.on_analysis)
        control_layout.addWidget(self.analysis_button)

        # 結束拍攝按鈕 layer 2
        self.end_button = QtWidgets.QPushButton("結束拍攝")
        self.end_button.setStyleSheet(BUTTON_STYLE)
        self.end_button.hide()
        self.end_button.clicked.connect(QtWidgets.QApplication.quit)
        control_layout.addWidget(self.end_button)

        layout.addWidget(control_widget)

    def _create_countdown_label(self, layout):
        """創建倒數計時標籤"""
        self.countdown_label = QtWidgets.QLabel("remaining time: -- s")
        self.countdown_label.setStyleSheet(COUNTDOWN_LABEL_STYLE)
        self.countdown_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.countdown_label)

    def _create_path_label(self, layout):
        """創建路徑顯示標籤"""
        self.path_label = QtWidgets.QLabel("save path: --")
        self.path_label.setStyleSheet(PATH_LABEL_STYLE)
        self.path_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.path_label)

    def _init_timers(self):
        """初始化計時器"""
        # 定時更新畫面
        self.frame_timer = QtCore.QTimer(self)
        self.frame_timer.timeout.connect(self.show_frame)
        self.frame_timer.start(100)  # 約10 fps

        # 倒數計時器
        self.countdown_timer = QtCore.QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

    def on_record_button(self):
        """處理錄製按鈕點擊"""
        if self.led_ctrl:
            # 按鈕先停用，避免重複點擊
            self.record_button.setEnabled(False)
            # 建立並啟動 LEDWorker
            self.led_worker = LEDWorker(self.led_ctrl)
            self.led_worker.finished.connect(self.start_record)  # LED 完成後呼叫
            self.led_worker.start()
        else:
            # 沒有 LED，直接錄影
            self.start_record()

    def set_save_folder(self, base_path: str, patient_id: str):
        """設定儲存資料夾"""
        folder = os.path.join(base_path, patient_id)
        os.makedirs(folder, exist_ok=True)
        self.save_folder = folder
        self.path_label.setText(f"儲存路徑: {self.save_folder}")

    def start_record(self):
        """開始錄製"""
        if not self.save_folder:
            QtWidgets.QMessageBox.warning(self, "錯誤", "尚未設定儲存資料夾！")
            return
        if self.is_recording:
            return

        self.is_recording = True
        self.record_duration = 40
        self.countdown_label.setText(f"剩餘時間: {self.record_duration} s")
        self.countdown_timer.start(1000)

    def update_countdown(self):
        """更新倒數計時"""
        self.record_duration -= 1
        self.countdown_label.setText(f"剩餘時間: {self.record_duration} s")
        if self.record_duration <= 0:
            self.stop_record()

    def stop_record(self):
        """停止錄製"""
        self.countdown_timer.stop()
        self.is_recording = False
        self.countdown_label.setText("錄製結束")
        self.record_button.setEnabled(True)
        # 顯示分析與結束按鈕
        self.analysis_button.show()
        self.end_button.show()

    def save_frame(self, frame):
        """儲存影格"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(self.save_folder, f"{timestamp}.jpg")
        cv2.imwrite(filename, frame)

    def show_frame(self):
        """顯示影格"""
        processed_frame, origin_frame = get_frames(self.cam, self.face_cascade)
        if processed_frame is None:
            return

        h, w, ch = processed_frame.shape
        bytes_per_line = ch * w
        q_img = QtGui.QImage(
            processed_frame.data,
            w,
            h,
            bytes_per_line,
            QtGui.QImage.Format.Format_BGR888,
        )
        self.cap_pic_region.setPixmap(QtGui.QPixmap.fromImage(q_img))

        if self.is_recording:
            self.save_frame(origin_frame)

    def on_analysis(self):
        """處理分析按鈕點擊"""
        # 發射請求，主程式接收並切換到分析頁面
        self.analysis_requested.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = PicCapingWindow()
    win.set_save_folder("./", "test_patient")
    win.show()
    sys.exit(app.exec())
