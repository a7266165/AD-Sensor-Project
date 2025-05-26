from PyQt6 import QtWidgets, QtCore, QtGui
from widger_helper import label_setup, entry_setup, button_setup
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
        
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Title
        self.grid1_box = QtWidgets.QWidget()
        self.grid1_box.setStyleSheet("")
        self.grid1_layout = QtWidgets.QHBoxLayout(self.grid1_box)
        self.title_label = label_setup("Camera", lambda: None)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(0, 0, 0); border: 0px;")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.grid1_layout.addWidget(self.title_label)

        self.main_layout.addWidget(self.grid1_box)
        
        # Camera view with frame
        self.camera_frame = QtWidgets.QFrame()
        self.camera_frame.setStyleSheet("background-color: #333333; border-radius: 8px;")
        self.camera_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.camera_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        self.camera_layout = QtWidgets.QVBoxLayout(self.camera_frame)
        self.camera_layout.setContentsMargins(10, 10, 10, 10)
        
        self.camera_label = QtWidgets.QLabel()
        self.camera_label.setStyleSheet("background-color: black; border-radius: 4px;")
        self.camera_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setMinimumHeight(500)
        self.camera_layout.addWidget(self.camera_label)
        
        self.main_layout.addWidget(self.camera_frame)
        
        # Control buttons layout
        self.button_frame = QtWidgets.QFrame()
        self.button_frame.setStyleSheet("background-color: #e0e0e0; border-radius: 8px;")
        self.button_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(20, 15, 20, 15)
        self.button_layout.setSpacing(15)
        
        button_style = """
            QPushButton {
                background-color: #4a86e8;
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
        
        # # Previous button
        # self.prev_button = QtWidgets.QPushButton("Previous")
        # self.prev_button.setStyleSheet(button_style)
        # self.prev_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
        # self.button_layout.addWidget(self.prev_button)
        
        # Spacer
        # self.button_layout.addStretch(1)
        
        # Record button
        self.record_button = QtWidgets.QPushButton("Start Recording")
        self.record_button.setStyleSheet(button_style.replace("#4a86e8", "#d54e4e"))
        self.button_layout.addWidget(self.record_button)
        
        # # Stop recording button
        # self.stop_button = QtWidgets.QPushButton("Stop Recording")
        # self.stop_button.setEnabled(False)  # Initially disabled
        # self.stop_button.setStyleSheet(button_style.replace("#4a86e8", "#4caf50"))
        # self.button_layout.addWidget(self.stop_button)
        
        # Spacer
        # self.button_layout.addStretch(1)
        
        # # Next button
        # self.next_button = QtWidgets.QPushButton("Next")
        # self.next_button.setStyleSheet(button_style)
        # self.next_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowForward))
        # self.button_layout.addWidget(self.next_button)
        
        # Add buttons frame to main layout
        self.main_layout.addWidget(self.button_frame)

    
    def update_frame(self, frame):
        """Update the camera feed with the latest frame."""
        print("Updating frame...")
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format.Format_BGR888)
        self.camera_label.setPixmap(QtGui.QPixmap.fromImage(q_image))
        
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    Form = CapWindow()
    Form.show()


    camera = CameraDevice(camera_type="RealSense")  # Change to "RealSense" for RealSense camera

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # Display the frame
        Form.update_frame(frame)
        
        key = cv2.waitKey(1) & 0xFF
        # Break the loop on 'q' key press
        if key == ord('q'):
            break
        

    sys.exit(app.exec())