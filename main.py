from ui.pages.patient_data_form import PatientDataFormWindow
from ui.pages.pic_caping_window import PicCapingWindow
from ui.pages.analysis_report_window import AnalysisReportWindow
from PyQt6 import QtWidgets, QtCore
import sys
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class PatientSession:
    """患者會話數據管理"""
    patient_data: dict
    save_base: str
    patient_id: str
    
    def validate(self) -> tuple[bool, str]:
        """驗證會話數據完整性"""
        if not self.save_base:
            return False, "請設定儲存資料夾"
        if not self.patient_id:
            return False, "請設定患者編號"
        if not self.patient_data:
            return False, "請填寫患者資料"
        return True, ""

class ADRecordingAnalysisWindow(QtWidgets.QMainWindow):
    """AD記錄分析主窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_session: Optional[PatientSession] = None
        self._setup_windows()
        self._connect_all_signals()
        
    def _setup_windows(self):
        """初始化子窗口"""
        self.info_window = PatientDataFormWindow()
        self.capture_window = PicCapingWindow()
        self.analysis_window: Optional[AnalysisReportWindow] = None
        
        # 設定窗口大小
        self.info_window.resize(600, 600)
        self.capture_window.resize(1024, 768)
        
    def _connect_all_signals(self):
        """連接信號槽"""
        self.info_window.data_ready.connect(self._on_patient_data_ready)
        self.info_window.validation_failed.connect(self._on_validation_failed)
        self.info_window.data_saved.connect(self._on_data_saved)
        self.info_window.save_failed.connect(self._on_save_failed)
        self.capture_window.analysis_requested.connect(self._on_analysis_requested)
        
    def start(self):
        """啟動應用程序"""
        self.info_window.show()
        
    def _on_patient_data_ready(self, patient_data: dict):
        """患者資料就緒時的回調"""
        try:
            # 創建會話
            self.current_session = PatientSession(
                patient_data=patient_data,
                save_base=self.info_window.save_path,
                patient_id=patient_data.get("ID", "")
            )
            
            # 驗證數據
            is_valid, error_msg = self.current_session.validate()
            if not is_valid:
                self._show_error(error_msg)
                return
                
            # 切換到拍照階段
            self._transition_to_capture()
            
        except Exception as e:
            self._show_error(f"數據處理錯誤: {str(e)}")
    
    def _on_validation_failed(self, error_message: str):
        """處理驗證失敗"""
        QtWidgets.QMessageBox.warning(self, "資料驗證失敗", error_message)
    
    def _on_data_saved(self, success_message: str):
        """處理數據保存成功"""
        QtWidgets.QMessageBox.information(self, "儲存成功", success_message)
    
    def _on_save_failed(self, error_message: str):
        """處理保存失敗"""
        QtWidgets.QMessageBox.critical(self, "儲存失敗", error_message)
            
    def _on_analysis_requested(self):
        """分析請求時的回調"""
        if not self.current_session:
            self._show_error("會話數據丟失，請重新開始")
            return
            
        try:
            self._transition_to_analysis()
        except Exception as e:
            self._show_error(f"分析啟動失敗: {str(e)}")
            
    def _transition_to_capture(self):
        """切換到拍照階段"""
        self.capture_window.set_save_folder(
            self.current_session.save_base, 
            self.current_session.patient_id
        )
        self.info_window.hide()
        self.capture_window.show()
        
    def _transition_to_analysis(self):
        """切換到分析階段"""
        self.capture_window.hide()
        
        # 準備分析所需的路徑
        csv_path = os.path.join(self.current_session.save_base, "AD_patient_data.csv")
        model_path = "./data/XGBoost.json"
        symmetry_csv_path = "./data/symmetry_all_pairs.csv"
        
        # 檢查必要文件是否存在
        if not self._validate_analysis_files(model_path, symmetry_csv_path):
            return
            
        # 創建分析窗口
        self.analysis_window = AnalysisReportWindow(
            self.current_session.save_base,
            self.current_session.patient_id,
            csv_path,
            symmetry_csv_path,
            model_path
        )
        
        self.analysis_window.show()
        QtCore.QTimer.singleShot(0, self.analysis_window.run_analysis)
        
    def _validate_analysis_files(self, model_path: str, symmetry_csv_path: str) -> bool:
        """驗證分析所需文件是否存在"""
        missing_files = []
        
        if not os.path.exists(model_path):
            missing_files.append(model_path)
        if not os.path.exists(symmetry_csv_path):
            missing_files.append(symmetry_csv_path)
            
        if missing_files:
            self._show_error(f"缺少必要文件:\n" + "\n".join(missing_files))
            return False
        return True
        
    def _show_error(self, message: str):
        """顯示錯誤訊息"""
        QtWidgets.QMessageBox.warning(self, "錯誤", message)
        
    def reset_session(self):
        """重置會話"""
        self.current_session = None
        if self.analysis_window:
            self.analysis_window.close()
            self.analysis_window = None
        self.capture_window.hide()
        self.info_window.show()

def main():
    """應用程序入口點"""
    app = QtWidgets.QApplication(sys.argv)
    
    # 設定應用程序屬性
    app.setApplicationName("AD Recording Analysis")
    app.setApplicationVersion("1.0.0")
    
    try:
        window = ADRecordingAnalysisWindow()
        window.start()
        return app.exec()
    except Exception as e:
        QtWidgets.QMessageBox.critical(
            None, "啟動錯誤", f"應用程序啟動失敗:\n{str(e)}"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())