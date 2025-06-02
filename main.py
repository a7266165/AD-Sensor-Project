from ui.pages.patient_data_form import PatientDataFormWindow
from ui.pages.pic_caping_window import PicCapingWindow
from ui.pages.analysis_report_window import AnalysisReportWindow
from PyQt6 import QtWidgets, QtCore
import sys
import os

class ADRecordingAnalysisWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.info_window = PatientDataFormWindow()
        self.capture_window = PicCapingWindow()
        self.info_window.set_next_callback(self.capture_pics)
        self.info_window.resize(600, 600)
        self.capture_window.resize(1024, 768)
        self.capture_window.analysis_requested.connect(self.show_analysis)

    def init(self):
        self.info_window.show()

    def capture_pics(self):
        data = self.info_window.get_data()
        save_base = self.info_window.save_path
        patient_id = data.get("ID")
        if not save_base or not patient_id:
            QtWidgets.QMessageBox.warning(
                self, "錯誤", "請先在表單中設定儲存資料夾與編號。"
            )
            return
        self.capture_window.set_save_folder(save_base, patient_id)
        self.info_window.hide()
        self.capture_window.show()

    def show_analysis(self):
        self.capture_window.hide()
        save_base = self.info_window.save_path
        patient_id = self.info_window.get_data().get("ID")
        csv_path = os.path.join(save_base, "AD_patient_data.csv")
        model_path = r".\data\XGBoost.json"  
        symmetry_csv_path = r".\data\symmetry_all_pairs.csv"
        self.analysis_window = AnalysisReportWindow(
            save_base, patient_id, csv_path, symmetry_csv_path, model_path
        )
        self.analysis_window.show()
        QtCore.QTimer.singleShot(0, self.analysis_window.run_analysis)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ADRecordingAnalysisWindow()
    window.init()
    sys.exit(app.exec())
