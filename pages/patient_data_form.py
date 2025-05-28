import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui
import pandas as pd
# 處理相對導入問題
try:
    # 當從子資料夾直接執行時
    import patient_data_form_style as styles
except ModuleNotFoundError:
    # 當從父資料夾執行時
    from . import patient_data_form_style as styles

class PatientDataFormWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        # 分離資料結構
        self.form_fields = {}  # 只存表單欄位元件
        self.buttons = {}      # 只存按鈕元件
        self.save_path = None  # 簡化儲存路徑管理
        self._next_callback = None
        self._build_ui()

    # ===== UI =====
    def _build_ui(self):
        self.root_layout = QtWidgets.QVBoxLayout(self)
        self._create_title_block()
        self._create_basic_info_block()
        self._create_q6ds_block()
        self._create_save_path_block()
        self._create_buttons_block()

    # ===== 第一母區塊 - title =====
    def _create_title_block(self):
        self.title = QtWidgets.QLabel("患者資料表單")
        self.title.setFixedHeight(40)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(styles.TITLE_STYLE)
        self.root_layout.addWidget(self.title)

    # ===== 第二母區塊 - basic information =====
    def _create_basic_info_block(self):
        parent = QtWidgets.QWidget()
        parent.setStyleSheet(styles.PARENT_WIDGET_STYLE)
        parent.setFixedHeight(200)
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(10)

        label = QtWidgets.QLabel("基本資料")
        label.setFixedHeight(20)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(styles.SUBTITLE_STYLE)
        layout.addWidget(label)

        # 內層填寫區
        grid_widget = QtWidgets.QWidget()
        grid_widget.setStyleSheet("border: 0px; background-color: transparent;")
        grid_layout = QtWidgets.QGridLayout(grid_widget)
        grid_layout.setSpacing(10)

        # 編號（必填）
        self.form_fields["ID"] = QtWidgets.QLineEdit()
        self.form_fields["ID"].setPlaceholderText("請輸入編號（必填）")
        self.form_fields["ID"].setStyleSheet(styles.INPUT_STYLE)
        grid_layout.addWidget(self._make_label("編號 *:"), 0, 0)
        grid_layout.addWidget(self.form_fields["ID"], 0, 1)

        # 拍攝日期
        self.form_fields["cap_date"] = QtWidgets.QDateEdit()
        self.form_fields["cap_date"].setDisplayFormat("yyyy-MM-dd")
        self.form_fields["cap_date"].setDate(QtCore.QDate.currentDate())
        self.form_fields["cap_date"].setCalendarPopup(True)
        self.form_fields["cap_date"].setStyleSheet(styles.INPUT_STYLE)
        grid_layout.addWidget(self._make_label("拍攝日期:"), 0, 2)
        grid_layout.addWidget(self.form_fields["cap_date"], 0, 3)

        # 性別（必填）
        gender_widget = QtWidgets.QWidget()
        gender_widget.setStyleSheet("border: 0px; background-color: transparent;")
        gender_layout = QtWidgets.QHBoxLayout(gender_widget)
        self.form_fields["gender"] = QtWidgets.QButtonGroup(self)
        for text, id_ in [("男", 1), ("女", 2)]:
            rb = QtWidgets.QRadioButton(text)
            rb.setStyleSheet(styles.LABEL_STYLE)
            gender_layout.addWidget(rb)
            self.form_fields["gender"].addButton(rb, id_)
        grid_layout.addWidget(self._make_label("生理性別 *:"), 1, 0)
        grid_layout.addWidget(gender_widget, 1, 1)

        # 生日
        self.form_fields["birthday"] = QtWidgets.QDateEdit()
        self.form_fields["birthday"].setDisplayFormat("yyyy-MM-dd")
        self.form_fields["birthday"].setDate(QtCore.QDate(1990, 1, 1))
        self.form_fields["birthday"].setCalendarPopup(True)
        self.form_fields["birthday"].setStyleSheet(styles.INPUT_STYLE)
        grid_layout.addWidget(self._make_label("生日:"), 1, 2)
        grid_layout.addWidget(self.form_fields["birthday"], 1, 3)

        # 教育年數（數值驗證）
        self.form_fields["education_years"] = QtWidgets.QLineEdit()
        self.form_fields["education_years"].setPlaceholderText("請輸入數字 (0-30)")
        self.form_fields["education_years"].setStyleSheet(styles.INPUT_STYLE)
        # 限制只能輸入數字
        validator = QtGui.QIntValidator(0, 30)
        self.form_fields["education_years"].setValidator(validator)
        grid_layout.addWidget(self._make_label("教育年數:"), 2, 0)
        grid_layout.addWidget(self.form_fields["education_years"], 2, 1)

        layout.addWidget(grid_widget)
        self.root_layout.addWidget(parent)

    # ===== 第三母區塊 - 6QDS =====
    def _create_q6ds_block(self):
        parent = QtWidgets.QWidget()
        parent.setStyleSheet(styles.PARENT_WIDGET_STYLE)
        parent.setFixedHeight(150)
        layout = QtWidgets.QGridLayout(parent)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("6QDS 量表 (評分範圍: 0-5)")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(styles.LABEL_STYLE)
        layout.addWidget(title, 0, 0, 1, 10)

        # 6QDS 評分欄位
        for i in range(1, 11):
            layout.addWidget(self._make_label(f"q{i}:"), 1, i-1)
            q_input = QtWidgets.QLineEdit()
            q_input.setPlaceholderText("0-5")
            q_input.setStyleSheet(styles.INPUT_STYLE)
            # 限制評分範圍 0-5
            validator = QtGui.QIntValidator(0, 5)
            q_input.setValidator(validator)
            layout.addWidget(q_input, 2, i-1)
            self.form_fields[f"q{i}"] = q_input

        self.root_layout.addWidget(parent)

    # ===== 第四母區塊 - save path =====
    def _create_save_path_block(self):
        parent = QtWidgets.QWidget()
        parent.setStyleSheet(styles.PARENT_WIDGET_STYLE)
        parent.setFixedHeight(80)
        layout = QtWidgets.QGridLayout(parent)
        layout.setSpacing(10)

        self.save_path_input = QtWidgets.QLineEdit()
        self.save_path_input.setReadOnly(True)
        self.save_path_input.setPlaceholderText("請選擇儲存資料夾")
        self.save_path_input.setStyleSheet(styles.INPUT_STYLE)
        layout.addWidget(self._make_label("儲存路徑 *:"), 0, 0)
        layout.addWidget(self.save_path_input, 0, 1)

        self.root_layout.addWidget(parent)

    # ===== 第五母區塊 - buttons =====
    def _create_buttons_block(self):
        parent = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(parent)
        layout.setSpacing(15)

        self.buttons["save_folder"] = QtWidgets.QPushButton("選擇儲存資料夾")
        self.buttons["save_folder"].setStyleSheet(styles.BUTTON_STYLE)
        self.buttons["save_folder"].clicked.connect(self.open_save_folder)
        layout.addWidget(self.buttons["save_folder"], 0, 0)

        self.buttons["clear"] = QtWidgets.QPushButton("清除全部")
        self.buttons["clear"].setStyleSheet(styles.BUTTON_STYLE)
        self.buttons["clear"].clicked.connect(self.clear_data)
        layout.addWidget(self.buttons["clear"], 0, 1)

        self.buttons["next"] = QtWidgets.QPushButton("儲存並下一步")
        self.buttons["next"].setStyleSheet(styles.BUTTON_STYLE)
        self.buttons["next"].clicked.connect(self._on_next)
        layout.addWidget(self.buttons["next"], 0, 3)

        self.root_layout.addWidget(parent)


    # ===== 以下為輔助函數 =====
    def _make_label(self, text):
        lbl = QtWidgets.QLabel(text)
        lbl.setStyleSheet(styles.LABEL_STYLE)
        return lbl

    def open_save_folder(self):
        """選擇儲存資料夾"""
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "選擇儲存資料夾",
            os.path.expanduser("~")  # 預設開啟使用者主目錄
        )
        if path:
            # 檢查資料夾寫入權限
            if os.access(path, os.W_OK):
                self.save_path = path
                self.save_path_input.setText(path)
            else:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "權限不足", 
                    "選擇的資料夾沒有寫入權限，請選擇其他資料夾"
                )

    def clear_data(self):
        """清除所有資料（附確認對話框）"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "確認清除",
            "確定要清除所有已填寫的資料嗎？",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self._clear_form_fields()

    def _clear_form_fields(self):
        """實際清除表單欄位的方法"""
        for field_name, widget in self.form_fields.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QButtonGroup):
                for button in widget.buttons():
                    button.setChecked(False)
            elif isinstance(widget, QtWidgets.QDateEdit):
                if field_name == "cap_date":
                    widget.setDate(QtCore.QDate.currentDate())
                elif field_name == "birthday":
                    widget.setDate(QtCore.QDate(1990, 1, 1))

    def set_next_callback(self, callback):
        """設定下一步按鈕的回調函數"""
        self._next_callback = callback

    def _on_next(self):
        """處理下一步按鈕點擊"""
        # 驗證資料
        validation_errors = self.validate_data()
        if validation_errors:
            error_message = "請修正以下問題：\n\n" + "\n".join(f"• {error}" for error in validation_errors)
            QtWidgets.QMessageBox.warning(self, "資料驗證失敗", error_message)
            return

        # 儲存資料
        if self.save_data():
            # 執行回調函數
            if callable(self._next_callback):
                self._next_callback()

    def validate_data(self):
        """驗證表單資料"""
        errors = []
        data = self.get_data()

        # 檢查必填欄位
        if not data.get('ID', '').strip():
            errors.append("編號為必填欄位")

        if not data.get('gender'):
            errors.append("請選擇生理性別")

        if not self.save_path:
            errors.append("請選擇儲存資料夾")

        # 檢查教育年數格式
        edu_years = data.get('education_years', '').strip()
        if edu_years and not edu_years.isdigit():
            errors.append("教育年數必須為數字")
        elif edu_years and (int(edu_years) < 0 or int(edu_years) > 30):
            errors.append("教育年數必須在 0-30 之間")

        # 檢查 6QDS 評分
        for i in range(1, 11):
            score = data.get(f'q{i}', '').strip()
            if score:  # 如果有填寫
                if not score.isdigit():
                    errors.append(f"q{i} 評分必須為數字")
                elif int(score) < 0 or int(score) > 5:
                    errors.append(f"q{i} 評分必須在 0-5 之間")

        return errors

    def get_data(self):
        """獲取表單資料"""
        data = {}
        for field_name, widget in self.form_fields.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                data[field_name] = widget.text().strip()
            elif isinstance(widget, QtWidgets.QButtonGroup):
                checked_button = widget.checkedButton()
                data[field_name] = checked_button.text() if checked_button else None
            elif isinstance(widget, QtWidgets.QDateEdit):
                data[field_name] = widget.date().toString("yyyy-MM-dd")
        
        return data

    def save_data(self):
        """儲存資料到 CSV 檔案"""
        try:
            data = self.get_data()
            df = pd.DataFrame([data])
            
            file_path = os.path.join(self.save_path, "AD_patient_data.csv")
            
            # 檢查檔案是否存在以決定是否寫入標題
            file_exists = os.path.isfile(file_path)
            mode = "a" if file_exists else "w"
            header = not file_exists
            
            # 儲存到 CSV
            df.to_csv(
                file_path, 
                mode=mode, 
                header=header, 
                index=False, 
                encoding="utf-8-sig"
            )
            
            # 顯示成功訊息
            QtWidgets.QMessageBox.information(
                self, 
                "儲存成功", 
                f"患者資料已成功儲存至：\n{file_path}"
            )
            
            return True
            
        except PermissionError:
            QtWidgets.QMessageBox.critical(
                self, 
                "儲存失敗", 
                "沒有權限寫入指定的資料夾，請檢查資料夾權限或選擇其他位置"
            )
            return False
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "儲存失敗", 
                f"儲存時發生錯誤：\n{str(e)}"
            )
            return False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = PatientDataFormWindow()
    win.resize(650, 650)
    win.show()
    sys.exit(app.exec())