import sys
import os
from PyQt6 import QtWidgets, QtCore
import pandas as pd
from widger_helper import (
    label_setup,
    entry_setup,
    combobox_setup,
    date_setup,
    button_setup,
)


class InfoWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.save_path_text = {}
        self.ui()

    def ui(self):
        # 創建根佈局
        self.root_layout = QtWidgets.QVBoxLayout(self)

        # 內容元件
        content_widget = QtWidgets.QWidget()
        layout_content = QtWidgets.QVBoxLayout(content_widget)
        layout_content.setSpacing(10)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        # 添加
        self.root_layout.addWidget(scroll_area)

        # # ===== Title =====#
        # # 1. 設定標題區塊
        # box_title = QtWidgets.QWidget()
        # box_title.setStyleSheet(None)
        # box_title.setFixedHeight(40)

        # # 2. 設定標題文字與樣式
        # content_title = QtWidgets.QLabel("表單")
        # content_title.setStyleSheet(
        #     "font-size: 24px; font-family: 微軟正黑體; font-weight: bold; border: 0px;"
        # )

        # # 3. 設定標題區塊的佈局
        # self.layout_title = QtWidgets.QGridLayout(box_title)
        # self.layout_title.addWidget(content_title, 0, 0)
        # self.layout_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # 置中
        # # ===== Title =====#

        # # ===== basic information =====#
        # # 1. 設定背景區塊
        # parent_box_basic_information = QtWidgets.QWidget()
        # parent_box_basic_information.setStyleSheet(
        #     "background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;"
        # )
        # self.layout_parent_box_basic_information = QtWidgets.QVBoxLayout(
        #     parent_box_basic_information
        # )

        # # 2. 設定基本資料母區塊
        # box_basic_information = QtWidgets.QWidget()
        # box_basic_information.setFixedHeight(40)
        # box_basic_information.setStyleSheet("border: 0px;")

        # # 2-1 設定基本資料母區塊的佈局
        # self.layout_title_basic_information = QtWidgets.QHBoxLayout(
        #     box_basic_information
        # )
        # self.layout_title_basic_information.setContentsMargins(0, 0, 0, 0)
        # self.layout_title_basic_information.setAlignment(
        #     QtCore.Qt.AlignmentFlag.AlignCenter
        # )
        # self.layout_parent_box_basic_information.addWidget(box_basic_information)

        # # 2-2. 設定標題文字與樣式
        # label_base_information = QtWidgets.QLabel("基本資料")
        # label_base_information.setStyleSheet(
        #     "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )

        # # 2-3. 加入佈局，最後再加入到父佈局裡
        # self.layout_title_basic_information.addWidget(label_base_information)

        # box_content_basic_information = QtWidgets.QWidget()
        # box_content_basic_information.setStyleSheet("border: 0px;")
        # self.layout_content_box_basic_information = QtWidgets.QGridLayout(box_content_basic_information)
        # self.layout_content_box_basic_information.setSpacing(15)
        # label_ID = label_setup(
        #     "編號 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(label_ID, 0, 0)
        # entry_ID = entry_setup(
        #     "請輸入編號", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(entry_ID, 0, 1)
        # self.widgets["ID"] = entry_ID

        # label_gender = label_setup(
        #     "性別 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(label_gender, 1, 0)
        # gender = combobox_setup(
        #     ["請選擇性別", "男", "女"],
        #     "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;",
        # )
        # self.layout_content_box_basic_information.addWidget(gender, 1, 1)
        # self.widgets["gender"] = gender

        # label_photography_year = label_setup(
        #     "拍攝日期 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(label_photography_year, 0, 2)
        # capture_pic_date = date_setup(
        #     self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(capture_pic_date, 0, 3)
        # self.widgets["capture_pic_date"] = capture_pic_date

        # label_birthday = label_setup(
        #     "生日 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(label_birthday, 1, 2)
        # birthday = date_setup(
        #     self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_content_box_basic_information.addWidget(birthday, 1, 3)
        # self.widgets["birthday"] = birthday

        # self.layout_parent_box_basic_information.addWidget(box_content_basic_information)
        # ==== basic information ====#

        # # ===== 6QDS =====#
        # title_6QDS = QtWidgets.QWidget()
        # title_6QDS.setStyleSheet("border: 0px;")
        # self.layout_title_6QDS = QtWidgets.QGridLayout(title_6QDS)
        # self.layout_title_6QDS.setSpacing(15)

        # label_6QDS = label_setup(
        #     "6QDS", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_title_6QDS.addWidget(label_6QDS, 0, 0, 1, 4)

        # box_6QDS = QtWidgets.QWidget()
        # box_6QDS.setStyleSheet("border: 0px;")
        # self.layout_box_6QDS = QtWidgets.QGridLayout(box_6QDS)
        # self.layout_box_6QDS.setSpacing(15)
        # q1 = label_setup(
        #     "q1 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q1, 0, 0)
        # entry_q1 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q1, 0, 1)
        # self.widgets["q1"] = entry_q1
        # q2 = label_setup(
        #     "q2 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q2, 0, 2)
        # entry_q2 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q2, 0, 3)
        # self.widgets["q2"] = entry_q2
        # q3 = label_setup(
        #     "q3 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q3, 0, 4)
        # entry_q3 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q3, 0, 5)
        # self.widgets["q3"] = entry_q3
        # q4 = label_setup(
        #     "q4 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q4, 0, 6)
        # entry_q4 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q4, 0, 7)
        # self.widgets["q4"] = entry_q4
        # q5 = label_setup(
        #     "q5 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q5, 0, 8)
        # entry_q5 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q5, 0, 9)
        # self.widgets["q5"] = entry_q5
        # q6 = label_setup(
        #     "q6 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q6, 1, 0)
        # entry_q6 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q6, 1, 1)
        # self.widgets["q6"] = entry_q6
        # q7 = label_setup(
        #     "q7 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q7, 1, 2)
        # entry_q7 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q7, 1, 3)
        # self.widgets["q7"] = entry_q7
        # q8 = label_setup(
        #     "q8 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q8, 1, 4)
        # entry_q8 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q8, 1, 5)
        # self.widgets["q8"] = entry_q8
        # q9 = label_setup(
        #     "q9 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q9, 1, 6)
        # entry_q9 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q9, 1, 7)
        # self.widgets["q9"] = entry_q9
        # q10 = label_setup(
        #     "q10 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(q10, 1, 8)
        # entry_q10 = entry_setup(
        #     "評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_box_6QDS.addWidget(entry_q10, 1, 9)
        # self.widgets["q10"] = entry_q10

        # parent_box_6QDS = QtWidgets.QWidget()
        # parent_box_6QDS.setStyleSheet(
        #     "background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;"
        # )
        # self.layout_parent_box_6QDS = QtWidgets.QVBoxLayout(parent_box_6QDS)
        # self.layout_parent_box_6QDS.addWidget(title_6QDS)
        # self.layout_parent_box_6QDS.addWidget(box_6QDS)
        # # ===== 6QDS =====#

        # # ===== savepath =====#
        # title_save_path = QtWidgets.QWidget()
        # title_save_path.setStyleSheet("border: 0px;")
        # title_save_path.setFixedHeight(40)
        # self.layout_title_save_path = QtWidgets.QGridLayout(title_save_path)
        # label_save_path = label_setup(
        #     "儲存路徑 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # self.layout_title_save_path.addWidget(label_save_path, 0, 0)

        # box_save_path = QtWidgets.QWidget()
        # box_save_path.setStyleSheet("border: 0px;")
        # self.layout_save_path = QtWidgets.QGridLayout(box_save_path)
        # entry_save_path = entry_setup(
        #     "", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
        # )
        # entry_save_path.setReadOnly(True)
        # self.layout_save_path.addWidget(entry_save_path, 1, 0, 1, 4)
        # self.save_path_text["entry_save_path"] = entry_save_path

        # parent_box_save_path = QtWidgets.QWidget()
        # parent_box_save_path.setStyleSheet(
        #     "background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;"
        # )
        # self.layout_parent_box_save_path = QtWidgets.QVBoxLayout(parent_box_save_path)
        # self.layout_parent_box_save_path.addWidget(title_save_path)
        # self.layout_parent_box_save_path.addWidget(box_save_path)
        # # ===== savepath =====#

        # # ===== buttons =====#
        # box_buttons = QtWidgets.QWidget()
        # # 6QDS.setFixedHeight(60)
        # self.layout_box_buttons = QtWidgets.QGridLayout(box_buttons)
        # self.layout_box_buttons.setSpacing(15)

        # button_save_folder = button_setup("選擇儲存資料夾", self.open_save_folder)
        # self.layout_box_buttons.addWidget(button_save_folder, 0, 0, 1, 2)

        # button_clear = button_setup("清除", self.clear_data)
        # self.layout_box_buttons.addWidget(button_clear, 0, 3)
        # self.widgets["button_clear"] = button_clear

        # button_save = button_setup("儲存", self.save_data)
        # self.layout_box_buttons.addWidget(button_save, 1, 0, 1, 2)
        # self.widgets["button_save"] = button_save

        # button_next = button_setup("下一步", lambda: print("下一步按鈕被點擊"))
        # self.layout_box_buttons.addWidget(button_next, 1, 3)
        # self.widgets["button_next"] = button_next
        # ===== buttons =====#

        # ===== scroll area =====#

        # ===== scroll area =====#

        # ==== Finally, add the grid layout to the main layout ====#
        # layout_content.addWidget(box_title)
        # layout_content.addWidget(parent_box_basic_information)
        # layout_content.addWidget(parent_box_6QDS)
        # layout_content.addWidget(parent_box_save_path)
        # layout_content.addWidget(box_buttons)
        # ===== Finish =====#

    def next_button(self, function):
        self.widgets["button_next"].clicked.connect(function)

    def get_data(self):
        data = {}
        for key, widget in self.widgets.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                data[key] = widget.text()
            elif isinstance(widget, QtWidgets.QComboBox):
                data[key] = widget.currentText()
            elif isinstance(widget, QtWidgets.QDateEdit):
                data[key] = widget.date().toString("yyyy-MM-dd")
            else:
                continue
        return data

    def open_save_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if folder_path:
            print(f"選擇的儲存資料夾: {folder_path}")
            self.save_path_text["save_path"] = folder_path
            self.save_path_text["entry_save_path"].setText(folder_path)

    def clear_data(self):
        for key, widget in self.widgets.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QtWidgets.QDateEdit):
                widget.setDate(QtCore.QDate.currentDate())
            else:
                pass

    def save_data(self):
        data = self.get_data()
        df = pd.DataFrame([data])

        save_path = self.save_path_text["save_path"]
        file_exists = os.path.isfile(save_path + "/AD_patient_data.csv")

        if file_exists is True:
            df.to_csv(
                save_path + "/AD_patient_data.csv",
                mode="a",
                header=False,
                index=False,
                encoding="utf-8-sig",
            )
            print(f"檔案接續儲存在:{save_path}AD_patient_data.csv")

        else:
            df.to_csv(
                save_path + "/AD_patient_data.csv",
                mode="w",
                header=True,
                index=False,
                encoding="utf-8-sig",
            )
            print(f"檔案第一次儲存在:{save_path}AD_patient_data.csv")

    # ===== Finish =====#


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    info_window = InfoWindow()
    info_window.setFixedSize(800, 600)
    info_window.show()
    sys.exit(app.exec())

    # import sys
    # import os
    # from PyQt6 import QtWidgets, QtCore
    # import pandas as pd
    # from widger_helper import (
    #     label_setup,
    #     entry_setup,
    #     combobox_setup,
    #     date_setup,
    #     button_setup,
    # )

    # # 全域樣式常數
    # STYLE_BOLD = "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
    # TITLE_STYLE = "font-size: 24px; font-family: 微軟正黑體; font-weight: bold;"
    # PANEL_STYLE = "background-color: rgb(214, 234, 248); border-radius: 20px; border: 2px solid black;"

    # class Section(QtWidgets.QWidget):
    #     def __init__(self, title: str, layout_content: QtWidgets.QLayout):
    #         super().__init__()
    #         self.setStyleSheet(PANEL_STYLE)
    #         layout = QtWidgets.QVBoxLayout(self)
    #         layout.addWidget(label_setup(title, STYLE_BOLD))
    #         layout.addLayout(layout_content)

    # class InfoWindow(QtWidgets.QFrame):
    #     def __init__(self):
    #         super().__init__()
    #         self.widgets = {}
    #         self.save_path = ""
    #         self.init_ui()

    #     def init_ui(self):
    #         self.setStyleSheet("QFrame { padding: 10px; }")
    #         root_layout = QtWidgets.QVBoxLayout(self)
    #         root_layout.setSpacing(10)

    #         # 標題
    #         title = label_setup("表單", TITLE_STYLE)
    #         title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    #         root_layout.addWidget(title)

    #         # 基本資料區塊
    #         form_layout = QtWidgets.QFormLayout()
    #         fields = [
    #             ("ID", entry_setup, ("請輸入編號", STYLE_BOLD)),
    #             ("gender", combobox_setup, (("請選擇性別", "男", "女"), STYLE_BOLD)),
    #             ("capture_pic_date", date_setup, (self, STYLE_BOLD)),
    #             ("birthday", date_setup, (self, STYLE_BOLD)),
    #         ]
    #         for key, creator, args in fields:
    #             widget = creator(*args)
    #             self.widgets[key] = widget
    #             label = label_setup(
    #                 {
    #                     "ID": "編號 :",
    #                     "gender": "性別 :",
    #                     "capture_pic_date": "拍攝日期 :",
    #                     "birthday": "生日 :",
    #                 }[key],
    #                 STYLE_BOLD,
    #             )
    #             form_layout.addRow(label, widget)
    #         root_layout.addWidget(Section("基本資料", form_layout))

    #         # 6QDS 區塊
    #         qds_layout = QtWidgets.QGridLayout()
    #         for i in range(10):
    #             row, col = divmod(i, 5)
    #             key = f"q{i+1}"
    #             lbl = label_setup(f"{key} :", STYLE_BOLD)
    #             entry = entry_setup("評分", STYLE_BOLD)
    #             self.widgets[key] = entry
    #             qds_layout.addWidget(lbl, row, col * 2)
    #             qds_layout.addWidget(entry, row, col * 2 + 1)
    #         root_layout.addWidget(Section("6QDS", qds_layout))

    #         # 儲存路徑區塊
    #         path_layout = QtWidgets.QHBoxLayout()
    #         path_widget = entry_setup("", STYLE_BOLD)
    #         path_widget.setReadOnly(True)
    #         self.widgets["save_path"] = path_widget
    #         path_layout.addWidget(path_widget)
    #         root_layout.addWidget(Section("儲存路徑", path_layout))

    #         # 按鈕區塊
    #         btn_layout = QtWidgets.QHBoxLayout()
    #         buttons = [
    #             ("選擇資料夾", self.open_save_folder),
    #             ("清除", self.clear_data),
    #             ("儲存", self.save_data),
    #             ("下一步", None),
    #         ]
    #         for text, slot in buttons:
    #             btn = button_setup(text, slot or (lambda: None))
    #             if text == "下一步":
    #                 self.widgets["button_next"] = btn
    #             btn_layout.addWidget(btn)
    #         root_layout.addLayout(btn_layout)

    #     def next_button(self, func):
    #         self.widgets["button_next"].clicked.connect(func)

    #     def get_data(self) -> dict:
    #         data = {}
    #         for k, w in self.widgets.items():
    #             if isinstance(w, QtWidgets.QLineEdit):
    #                 data[k] = w.text()
    #             elif isinstance(w, QtWidgets.QComboBox):
    #                 data[k] = w.currentText()
    #             elif isinstance(w, QtWidgets.QDateEdit):
    #                 data[k] = w.date().toString("yyyy-MM-dd")
    #         return data

    #     def open_save_folder(self):
    #         folder = QtWidgets.QFileDialog.getExistingDirectory(self)
    #         if folder:
    #             self.save_path = folder
    #             self.widgets["save_path"].setText(folder)

    #     def clear_data(self):
    #         for w in self.widgets.values():
    #             if isinstance(w, QtWidgets.QLineEdit):
    #                 w.clear()
    #             elif isinstance(w, QtWidgets.QComboBox):
    #                 w.setCurrentIndex(0)
    #             elif isinstance(w, QtWidgets.QDateEdit):
    #                 w.setDate(QtCore.QDate.currentDate())

    #     def save_data(self):
    #         data = self.get_data()
    #         if not self.save_path:
    #             QtWidgets.QMessageBox.warning(self, "錯誤", "請先選擇儲存資料夾")
    #             return
    #         df = pd.DataFrame([data])
    #         path = os.path.join(self.save_path, "AD_patient_data.csv")
    #         df.to_csv(
    #             path,
    #             mode="a" if os.path.isfile(path) else "w",
    #             header=not os.path.isfile(path),
    #             index=False,
    #             encoding="utf-8-sig",
    #         )

    # if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = InfoWindow()
    win.setFixedSize(800, 1000)
    win.show()
    sys.exit(app.exec())
