import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui
import pandas as pd
from ui.styles.patient_data_form_style import (
BUTTON_STYLE, 
 PARENT_WIDGET_STYLE, 
 TITLE_STYLE, 
 SUBTITLE_STYLE, 
 LABEL_STYLE, 
 INPUT_STYLE)

class PatientDataFormWindow(QtWidgets.QFrame):
    data_ready = QtCore.pyqtSignal(dict) 
    validation_failed = QtCore.pyqtSignal(str)
    data_saved = QtCore.pyqtSignal(str)
    save_failed = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_attributes()
        self._init_ui()

    def _init_window(self):
        self.setWindowTitle("患者資料表單")
        self.resize(600, 600)

    def _init_attributes(self):
        self.form_fields = {}
        self.buttons = {}
        self.save_path = None

    # ===== UI ===== #
    def _init_ui(self):
        self.root_layout = QtWidgets.QVBoxLayout(self) # (layer 0)
        self._create_title_block()
        self._create_basic_info_block() 
        self._create_q6ds_block()
        self._create_save_path_block()
        self._create_buttons_block() 

    # ===== 第一母區塊 - title ===== # (layer 1)
    def _create_title_block(self):
        title_block = QtWidgets.QLabel("患者資料表單")
        title_block.setFixedHeight(40)
        title_block.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_block.setStyleSheet(TITLE_STYLE)
        self.root_layout.addWidget(title_block)

    # ===== 第二母區塊 - basic information ===== # (layer 1)
    def _create_basic_info_block(self):
        # 建立基本資料區塊根容器
        basic_info_block = QtWidgets.QWidget()
        basic_info_block.setStyleSheet(PARENT_WIDGET_STYLE)
        basic_info_block.setFixedHeight(200)

        basic_info_block_layout = QtWidgets.QVBoxLayout(basic_info_block)
        basic_info_block_layout.setSpacing(10)

        basic_info_block_label = QtWidgets.QLabel("基本資料")  # (layer 2)
        basic_info_block_label.setFixedHeight(20)
        basic_info_block_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        basic_info_block_label.setStyleSheet(SUBTITLE_STYLE)
        basic_info_block_layout.addWidget(basic_info_block_label)

        basic_info_grid_block = QtWidgets.QWidget()  # (layer 2)
        basic_info_grid_block.setStyleSheet("border: 0px; background-color: transparent;")
        basic_info_grid_layout = QtWidgets.QGridLayout(basic_info_grid_block)
        basic_info_grid_layout.setSpacing(10)

        self.form_fields["ID"] = QtWidgets.QLineEdit()  # (layer 3)
        self.form_fields["ID"].setPlaceholderText("請輸入編號（必填）")
        self.form_fields["ID"].setStyleSheet(INPUT_STYLE)
        basic_info_grid_layout.addWidget(self._make_label("編號 *:"), 0, 0)
        basic_info_grid_layout.addWidget(self.form_fields["ID"], 0, 1)

        self.form_fields["cap_date"] = QtWidgets.QDateEdit()  # (layer 3)
        self.form_fields["cap_date"].setDisplayFormat("yyyy-MM-dd")
        self.form_fields["cap_date"].setDate(QtCore.QDate.currentDate())
        self.form_fields["cap_date"].setCalendarPopup(True)
        self.form_fields["cap_date"].setStyleSheet(INPUT_STYLE)
        basic_info_grid_layout.addWidget(self._make_label("拍攝日期:"), 0, 2)
        basic_info_grid_layout.addWidget(self.form_fields["cap_date"], 0, 3)

        basic_info_gender_block = QtWidgets.QWidget()  # (layer 3)
        basic_info_gender_block.setStyleSheet("border: 0px; background-color: transparent;")
        basic_info_gender_layout = QtWidgets.QHBoxLayout(basic_info_gender_block)
        self.form_fields["gender"] = QtWidgets.QButtonGroup(self)  # (layer 3)
        for text, id_ in [("男", 1), ("女", 2)]:
            rb = QtWidgets.QRadioButton(text)
            rb.setStyleSheet(LABEL_STYLE)
            basic_info_gender_layout.addWidget(rb)
            self.form_fields["gender"].addButton(rb, id_)
        basic_info_grid_layout.addWidget(self._make_label("生理性別 *:"), 1, 0)
        basic_info_grid_layout.addWidget(basic_info_gender_block, 1, 1)

        self.form_fields["birthday"] = QtWidgets.QDateEdit()  # (layer 3)
        self.form_fields["birthday"].setDisplayFormat("yyyy-MM-dd")
        self.form_fields["birthday"].setDate(QtCore.QDate(1990, 1, 1))
        self.form_fields["birthday"].setCalendarPopup(True)
        self.form_fields["birthday"].setStyleSheet(INPUT_STYLE)
        basic_info_grid_layout.addWidget(self._make_label("生日:"), 1, 2)
        basic_info_grid_layout.addWidget(self.form_fields["birthday"], 1, 3)

        self.form_fields["education_years"] = QtWidgets.QLineEdit()  # (layer 3)
        self.form_fields["education_years"].setPlaceholderText("請輸入數字 (0-30)")
        self.form_fields["education_years"].setStyleSheet(INPUT_STYLE)
        basic_validator = QtGui.QIntValidator(0, 30)  # 限制輸入為 0-30 的整數
        self.form_fields["education_years"].setValidator(basic_validator)
        basic_info_grid_layout.addWidget(self._make_label("教育年數:"), 2, 0)
        basic_info_grid_layout.addWidget(self.form_fields["education_years"], 2, 1)

        basic_info_block_layout.addWidget(basic_info_grid_block)
        self.root_layout.addWidget(basic_info_block)


    # ===== 第三母區塊 - 6QDS ===== # (layer 1)
    def _create_q6ds_block(self):
        q6ds_block = QtWidgets.QWidget()
        q6ds_block.setStyleSheet(PARENT_WIDGET_STYLE)
        q6ds_block.setFixedHeight(150)
        layout = QtWidgets.QGridLayout(q6ds_block)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("6QDS 量表 (評分範圍: 0-5)") # (layer 2)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(LABEL_STYLE)
        layout.addWidget(title, 0, 0, 1, 10)

        # 6QDS 評分欄位
        for i in range(1, 11):
            layout.addWidget(self._make_label(f"q{i}:"), 1, i - 1)
            q_input = QtWidgets.QLineEdit() # (layer 3)
            q_input.setPlaceholderText("0-5")
            q_input.setStyleSheet(INPUT_STYLE)
            validator = QtGui.QIntValidator(0, 5)  # 限制評分範圍 0-5
            q_input.setValidator(validator)
            layout.addWidget(q_input, 2, i - 1)
            self.form_fields[f"q{i}"] = q_input

        self.root_layout.addWidget(q6ds_block)

    # ===== 第四母區塊 - save path ===== # (layer 1)
    def _create_save_path_block(self):
        save_path_block = QtWidgets.QWidget()
        save_path_block.setStyleSheet(PARENT_WIDGET_STYLE)
        save_path_block.setFixedHeight(80)
        layout = QtWidgets.QGridLayout(save_path_block)
        layout.setSpacing(10)

        self.save_path_input = QtWidgets.QLineEdit() # (layer 2)
        self.save_path_input.setReadOnly(True)
        self.save_path_input.setPlaceholderText("請選擇儲存資料夾")
        self.save_path_input.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self._make_label("儲存路徑 *:"), 0, 0)
        layout.addWidget(self.save_path_input, 0, 1)

        self.root_layout.addWidget(save_path_block)

    # ===== 第五母區塊 - buttons ===== # (layer 1)
    def _create_buttons_block(self):
        buttons_block = QtWidgets.QWidget()
        buttons_layout = QtWidgets.QGridLayout(buttons_block)
        buttons_layout.setSpacing(15)

        self.buttons["save_folder"] = QtWidgets.QPushButton("選擇儲存資料夾") # (layer 2)
        self.buttons["save_folder"].setStyleSheet(BUTTON_STYLE)
        self.buttons["save_folder"].clicked.connect(self._open_save_folder)
        buttons_layout.addWidget(self.buttons["save_folder"], 0, 0)

        self.buttons["clear"] = QtWidgets.QPushButton("清除全部") # (layer 2)
        self.buttons["clear"].setStyleSheet(BUTTON_STYLE)
        self.buttons["clear"].clicked.connect(self._clear_data)
        buttons_layout.addWidget(self.buttons["clear"], 0, 1)

        self.buttons["next"] = QtWidgets.QPushButton("儲存並下一步") # (layer 2)
        self.buttons["next"].setStyleSheet(BUTTON_STYLE)
        self.buttons["next"].clicked.connect(self._on_next)
        buttons_layout.addWidget(self.buttons["next"], 0, 3)

        self.root_layout.addWidget(buttons_block)

    # ===== 輔助函數 =====
    def _make_label(self, text):
        lbl = QtWidgets.QLabel(text)
        lbl.setStyleSheet(LABEL_STYLE)
        return lbl

    def _open_save_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "選擇儲存資料夾", os.path.expanduser("~")  # 預設開啟使用者主目錄
        )
        if path:
            if os.access(path, os.W_OK):
                self.save_path = path
                self.save_path_input.setText(path)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "權限不足", "選擇的資料夾沒有寫入權限，請選擇其他資料夾"
                )

    def _clear_data(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "確認清除",
            "確定要清除所有已填寫的資料嗎？",
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self._clear_form_fields()

    def _clear_form_fields(self):
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

    def _on_next(self):
        # 驗證資料
        validation_errors = self._validate_data()
        if validation_errors:
            error_message = "請修正以下問題：\n\n" + "\n".join(
                f"• {error}" for error in validation_errors
            )
            self.validation_failed.emit(error_message)
            return

        # 儲存資料
        if self._save_data():
            data = self._get_data()
            self.data_ready.emit(data)

    def _validate_data(self):
        errors = []
        data = self._get_data()

        # 檢查必填欄位
        if not data.get("ID", "").strip():
            errors.append("編號為必填欄位")

        if not data.get("gender"):
            errors.append("請選擇生理性別")

        if not self.save_path:
            errors.append("請選擇儲存資料夾")

        # 檢查教育年數格式
        edu_years = data.get("education_years", "").strip()
        if edu_years and not edu_years.isdigit():
            errors.append("教育年數必須為數字")
        elif edu_years and (int(edu_years) < 0 or int(edu_years) > 30):
            errors.append("教育年數必須在 0-30 之間")

        # 檢查 6QDS 評分
        for i in range(1, 11):
            score = data.get(f"q{i}", "").strip()
            if score:  # 如果有填寫
                if not score.isdigit():
                    errors.append(f"q{i} 評分必須為數字")
                elif int(score) < 0 or int(score) > 5:
                    errors.append(f"q{i} 評分必須在 0-5 之間")

        return errors

    def _get_data(self):
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

    def _save_data(self):
        try:
            data = self._get_data()
            df = pd.DataFrame([data])

            file_path = os.path.join(self.save_path, "AD_patient_data.csv")

            # 檢查檔案是否存在以決定是否寫入標題
            file_exists = os.path.isfile(file_path)
            mode = "a" if file_exists else "w"
            header = not file_exists

            # 儲存到 CSV
            df.to_csv(
                file_path, mode=mode, header=header, index=False, encoding="utf-8-sig"
            )

            # 發射保存成功信號
            self.data_saved.emit(f"患者資料已成功儲存至：\n{file_path}")
            return True

        except PermissionError:
            error_msg = "沒有權限寫入指定的資料夾，請檢查資料夾權限或選擇其他位置"
            self.save_failed.emit(error_msg)
            return False

        except Exception as e:
            error_msg = f"儲存時發生錯誤：\n{str(e)}"
            self.save_failed.emit(error_msg)
            return False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = PatientDataFormWindow()
    win.resize(650, 650)
    win.show()
    sys.exit(app.exec())
