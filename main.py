# from _1_Personal_GUI import InfoWindow
# from _2_Photography_window import CapWindow
# from PyQt6 import QtWidgets
# import sys


# # from LED_GUI import LEDWindow, LEDPresenter
# class ADRecordingAnalysisWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.info_window = InfoWindow()
#         self.info_window.next_button(self.capture_pics)
#         self.capture_window = CapWindow()
#         self.info_window.resize(600, 600)
#         self.capture_window.resize(600, 1000)

#     # 初始窗口
#     def init(self):
#         self.info_window.show()

#     def capture_pics(self):
#         self.info_window.hide()
#         self.capture_window.show()

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = ADRecordingAnalysisWindow()
#     window.init()
#     sys.exit(app.exec())

# main.py
from pages.patient_data_form import PatientDataFormWindow
from pages.pic_caping_window import PicCapingWindow
from pages.analysis_report_window import AnalysisReportWindow
from PyQt6 import QtWidgets, QtCore
import sys
import os


class ADRecordingAnalysisWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.info_window = PatientDataFormWindow()
        self.capture_window = PicCapingWindow()
        # 綁定下一步按鈕，傳遞儲存路徑與編號
        self.info_window.set_next_callback(self.capture_pics)
        self.info_window.resize(600, 600)
        self.capture_window.resize(1024, 768)
        # 綁定即時分析訊號
        self.capture_window.analysis_requested.connect(self.show_analysis)

    def init(self):
        self.info_window.show()

    def capture_pics(self):
        # 取得畫面1的輸入與路徑
        data = self.info_window.get_data()
        save_base = self.info_window.save_path
        patient_id = data.get("ID")
        if not save_base or not patient_id:
            QtWidgets.QMessageBox.warning(
                self, "錯誤", "請先在表單中設定儲存資料夾與編號。"
            )
            return
        # 設定畫面2儲存路徑
        self.capture_window.set_save_folder(save_base, patient_id)
        self.info_window.hide()
        self.capture_window.show()

    def show_analysis(self):
        # 隱藏拍攝視窗
        self.capture_window.hide()
        # 建立並顯示分析結果視窗
        save_base = self.info_window.save_path
        patient_id = self.info_window.get_data().get("ID")
        # CSV 與模型路徑
        csv_path = os.path.join(save_base, "AD_patient_data.csv")
        model_path = r"C:\Users\4080\Desktop\python\AD-Sensor-Project\data\XGBoost.json"  # 替換為實際模型路徑
        symmetry_csv_path = r'C:\Users\4080\Desktop\python\AD-Sensor-Project\data\symmetry_all_pairs.csv'
        self.analysis_window = AnalysisReportWindow(save_base, patient_id, csv_path, symmetry_csv_path, model_path)
        self.analysis_window.show()
        QtCore.QTimer.singleShot(0, self.analysis_window.run_analysis)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ADRecordingAnalysisWindow()
    window.init()
    sys.exit(app.exec())
