import sys
import os
from PyQt6 import QtWidgets, QtCore
import pandas as pd

# TODO: (1) 把樣式表移到外部檔案 (2) 使用迴圈自動產生 Q6DS 問卷 (3) 區塊化 UI 建構流程

button_style = """
QPushButton {
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
    border: 1.5px solid black;
    border-radius: 12px;
    text-align: center;
    font-family: "微軟正黑體";
    font-size: 20px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: rgb(174, 214, 241);
}
QPushButton:pressed {
    background-color: rgb(30, 144, 255);
    color: rgb(255, 255, 255);
    border: 1.5px dashed black;
}
"""

class InfoWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.basic_infos = {}
        self.save_path_text = {}
        self.ui()

    def ui(self):
        # 設定根佈局(layer 0)
        root_layout = QtWidgets.QVBoxLayout(self)

        # 創建 & 設定內容區塊(layer 1)
        content_widget = QtWidgets.QWidget()
        content_scroll_area = QtWidgets.QScrollArea() # 將內容元件包裝為可滾動
        content_scroll_area.setWidgetResizable(True)
        content_scroll_area.setWidget(content_widget)
        content_layout = QtWidgets.QVBoxLayout(content_widget) # 內容區塊(layer 1)的排版
        content_layout.setSpacing(10)

        # 在根佈局(layer 0)添加內容區塊(layer 1)
        root_layout.addWidget(content_scroll_area)

        # ===== 第一母區塊 - Title =====#
        # 創建 & 設定標題區塊(layer 2)
        title_content = QtWidgets.QLabel("表單")
        title_content.setFixedHeight(40)  # 與原本 title_widget 一樣的高度
        title_content.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # 文字置中
        title_content.setStyleSheet(
            "font-size: 24px;"
            "font-family: 微軟正黑體;"
            "font-weight: bold;"
            "border: 0px;"
        )
        

        # 將標題區塊(layer 2)加入到內容區塊(layer 1)的排版
        content_layout.addWidget(title_content)
        # ===== 第一母區塊 - Title =====#

        # ===== 第二母區塊 - basic information =====#
        # 創建 & 設定基本資料背景區塊(layer 2)
        basic_info_parent_widget = QtWidgets.QWidget()
        basic_info_parent_widget.setStyleSheet(
            "background-color: rgb(214, 234, 248); border-radius: 20px; border: 2px solid black; border-radius: 20px;"
        )
        basic_info_parent_widget_layout = QtWidgets.QVBoxLayout(
            basic_info_parent_widget
        )
        basic_info_parent_widget_layout.setSpacing(10)
        basic_info_parent_widget.setFixedHeight(200) # 調整基本資料背景區塊(layer 2)的大小

        # 創建 & 設定基本資料標題區塊(layer 3)
        label_base_info = QtWidgets.QLabel("基本資料")
        label_base_info.setFixedHeight(20)  # 高度同原本 widget
        label_base_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # 置中
        label_base_info.setStyleSheet(
            "font-size: 20px;"
            "font-family: 微軟正黑體;"
            "font-weight: bold;"
            "border: 0px;"
        )

        # 創建 & 設定基本資料填寫區塊(layer 3) 
        basic_info_input_widget = QtWidgets.QWidget()
        basic_info_input_widget.setStyleSheet("border: 0px;")
        basic_info_input_widget_layout = QtWidgets.QGridLayout(basic_info_input_widget) # 基本資料填寫區塊(layer 3)的排版
        basic_info_input_widget_layout.setSpacing(10)

        # 建立 & 設定標籤標題、填寫區塊(layer 4) 
        ID_label =QtWidgets.QLabel("編號 :")
        ID_label.setStyleSheet("font-size: 16px; font-family: 微軟正黑體; font-weight: bold; border: 0px")
        ID_input = QtWidgets.QLineEdit()
        ID_input.setPlaceholderText("請輸入編號")  # 設定提示文字
        ID_input.setStyleSheet("font-size: 16px; font-family: 微軟正黑體; background-color: rgb(255, 255, 255); font-weight: bold; border: 1px solid black; border-radius: 5px")  # 設定字型大小
        
        # 建立 & 設定拍攝日期標籤、填寫區塊(layer 4)
        cap_date_label = QtWidgets.QLabel("拍攝日期 :")
        cap_date_label.setStyleSheet("font-size: 16px; font-family: 微軟正黑體; font-weight: bold;" " border: 0px")
        cap_date_input = QtWidgets.QDateEdit(self)  # 建立日期調整元件
        cap_date_input.setDisplayFormat('yyyy-MM-dd')  # 設定顯示格式
        cap_date_input.setDate(QtCore.QDate.currentDate())
        cap_date_input.setKeyboardTracking(True)
        cap_date_input.setCalendarPopup(True)  # 設定為彈出式日曆
        cap_date_input.setStyleSheet(f'font-size: 16px; font-family: 微軟正黑體; font-weight: bold; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')


        # 建立 & 設定性別標籤、填寫區塊(layer 4)
        gender_label = QtWidgets.QLabel("生理性別：")
        gender_label.setStyleSheet(
            "font-size: 16px; font-family: 微軟正黑體; font-weight: bold; border: 0px;"
        )
        gender_input = QtWidgets.QWidget()
        gender_input_layout =QtWidgets.QHBoxLayout(gender_input)

        # 建立 & 設定性別選擇按鈕(layer 5)
        male_radio = QtWidgets.QRadioButton("男")
        female_radio = QtWidgets.QRadioButton("女")
        for rb in (male_radio, female_radio):
            rb.setStyleSheet(
                "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
                
            )
            # 將layer 5 加入到性別填寫區塊layer 4的排版
            gender_input_layout.addWidget(rb)
        gender_group = QtWidgets.QButtonGroup(self) # 把RadioButton 加入 ButtonGroup，確保互斥
        gender_group.addButton(male_radio, 1)
        gender_group.addButton(female_radio, 2)
   
        # 建立生日標籤區塊(layer 4)
        birthday_label = QtWidgets.QLabel("生日 :")
        birthday_label.setStyleSheet(
            "font-size: 16px; font-family: 微軟正黑體; font-weight: bold; border: 0px"
        )

        # 建立生日填寫區塊(layer 4)
        birthday_input = QtWidgets.QDateEdit(self)  # 建立日期調整元件
        birthday_input.setDisplayFormat('yyyy-MM-dd')  # 設定顯示格式
        birthday_input.setDate(QtCore.QDate(1990, 1, 1))
        birthday_input.setKeyboardTracking(True)
        birthday_input.setCalendarPopup(True)  # 設定為彈出式日曆
        birthday_input.setStyleSheet(f'font-size: 16px; font-family: 微軟正黑體; font-weight: bold; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')

        # 將基本資料填寫區塊(layer 3)的內容加入到 basic_infos 字典中
        self.basic_infos["ID"] = ID_input
        self.basic_infos["gender"] = gender_group
        self.basic_infos["cap_date"] = cap_date_input
        self.basic_infos["birthday"] = birthday_input

        # 將layer 4加入到基本資料填寫區塊layer 3的排版
        basic_info_input_widget_layout.addWidget(gender_label, 1, 0)
        basic_info_input_widget_layout.addWidget(gender_input, 1, 1)
        basic_info_input_widget_layout.addWidget(birthday_label, 1, 2)
        basic_info_input_widget_layout.addWidget(birthday_input, 1, 3)
        basic_info_input_widget_layout.addWidget(ID_label, 0, 0)
        basic_info_input_widget_layout.addWidget(ID_input, 0, 1)
        basic_info_input_widget_layout.addWidget(cap_date_label, 0, 2)
        basic_info_input_widget_layout.addWidget(cap_date_input, 0, 3)

        # 標題區塊(layer 3)加入到基本資料背景區塊(layer 2)的排版
        basic_info_parent_widget_layout.addWidget(label_base_info)

        # basic_info_input_widget(layer 3)加入到基本資料背景區塊(layer 2)的排版
        basic_info_parent_widget_layout.addWidget(basic_info_input_widget)

        # 將基本資料背景區塊(layer 2)加入到內容區塊(layer 1)的排版
        content_layout.addWidget(basic_info_parent_widget)
        # ===== 第二母區塊 - basic information =====#

        # ===== 第三母區塊 - 6QDS ===== #
        # 創建 & 設定6QDS問卷區塊(layer 2)
        Q6DS_parent_widget = QtWidgets.QWidget()
        Q6DS_parent_widget.setStyleSheet("background-color: rgb(214, 234, 248); border: 2px solid black; border-radius: 20px;")
        Q6DS_parent_widget.setFixedHeight(150) # 調整6QDS問卷區塊(layer 2)的大小
        Q6DS_parent_widget_layout = QtWidgets.QGridLayout(Q6DS_parent_widget)
        Q6DS_parent_widget_layout.setSpacing(10)

        # 創建 & 設定6QDS問卷標題區塊(layer 3)
        Q6DS_label_widget = QtWidgets.QLabel("6QDS")
        Q6DS_label_widget.setStyleSheet(f"font-size: 16px; font-family: 微軟正黑體; font-weight: bold; border: 0px")
        Q6DS_label_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # 文字置中

        # 創建 & 設定6QDS問卷填寫區塊(layer 3)
        Q6DS_answer_widget = QtWidgets.QWidget()
        Q6DS_answer_widget.setStyleSheet("border: 0px;")
        Q6DS_answer_widget_layout = QtWidgets.QGridLayout(Q6DS_answer_widget)
        Q6DS_answer_widget_layout.setSpacing(10)
        
        for i in range(1, 11):
            # 創建 & 設定問卷問題標籤(layer 4)
            question_label = QtWidgets.QLabel(f"q{i} :")
            question_label.setStyleSheet(
                "font-size: 16px; font-family: 微軟正黑體; font-weight: bold; border: 0px;"
            )
            Q6DS_answer_widget_layout.addWidget(question_label, 0, i - 1)
            # 創建 & 設定問卷問題輸入框(layer 4)
            question_input = QtWidgets.QLineEdit()
            question_input.setPlaceholderText("評分")
            question_input.setStyleSheet(
                "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
                "background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px;"
                )
            Q6DS_answer_widget_layout.addWidget(question_input, 1, i - 1)

            # TODO: 要把輸入值用另一個字典儲存
            self.basic_infos[f"q{i}"] = question_input  # 將每個問題的輸入框加入到 basic_infos 字典中

        # 將6QDS問卷標題區塊(layer 3)加入到6QDS問卷區塊(layer 2)的排版
        Q6DS_parent_widget_layout.addWidget(Q6DS_label_widget)

        # 將6QDS問卷填寫區塊(layer 3)加入到6QDS問卷區塊(layer 2)的排版
        Q6DS_parent_widget_layout.addWidget(Q6DS_answer_widget)

        # 將6QDS問卷區塊(layer 2)加入到內容區塊(layer 1)的排版
        content_layout.addWidget(Q6DS_parent_widget)
        # ===== 第三母區塊 - 6QDS ===== #

        # ===== 第四母區塊 - save path ===== #
        # 創建 & 設定儲存路徑標題區塊(layer 2)
        save_path_parent_widget = QtWidgets.QWidget()
        save_path_parent_widget.setStyleSheet("background-color: rgb(214, 234, 248); border: 2px solid black; border-radius: 20px;")
        save_path_parent_widget.setFixedHeight(80) # 調整儲存路徑區塊(layer 2)的大小
        save_path_parent_widget_layout = QtWidgets.QGridLayout(save_path_parent_widget)

        # 創建 & 設定儲存路徑標籤區塊(layer 3)
        save_path_label = QtWidgets.QLabel("儲存路徑 :")
        save_path_label.setStyleSheet(
            "font-size: 16px; font-family: 微軟正黑體; font-weight: bold; border: 0px;"
        )

        # 創建 & 設定儲存路徑填寫區塊(layer 3)的輸入框
        save_path_input = QtWidgets.QLineEdit()
        save_path_input.setPlaceholderText("")
        save_path_input.setStyleSheet(
            "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;"
            " background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px;"
        )
        save_path_input.setReadOnly(True)

        # 將儲存路徑填寫區塊(layer 3)的內容加入到 save_path_text 字典中
        self.save_path_text["save_path_input"] = save_path_input

        # 將儲存路徑標籤區塊(layer 3)加入到儲存路徑標題區塊(layer 2)的排版
        save_path_parent_widget_layout.addWidget(save_path_label, 0, 0)

        # 將儲存路徑填寫區塊(layer 3)加入到儲存路徑標題區塊(layer 2)的排版
        save_path_parent_widget_layout.addWidget(save_path_input, 0, 1)

        # 將儲存路徑標題區塊(layer 2)加入到內容區塊(layer 1)的排版
        content_layout.addWidget(save_path_parent_widget)
        # ===== 第四母區塊 - savepath =====#

        # ===== 第五母區塊 - buttons =====#
        # 創建 & 設定按鈕區塊(layer 2)
        buttons_parent_widget = QtWidgets.QWidget()
        buttons_parent_widget_layout = QtWidgets.QGridLayout(buttons_parent_widget)
        buttons_parent_widget_layout.setSpacing(15)

        # 創建 & 設定路徑選擇按鈕(layer 3)
        button_save_folder = QtWidgets.QPushButton("選擇儲存資料夾")
        button_save_folder.clicked.connect(self.open_save_folder)
        button_save_folder.setStyleSheet(button_style)
        buttons_parent_widget_layout.addWidget(button_save_folder, 0, 0)

        # 創建 & 設定清除按鈕(layer 3)
        button_clear = QtWidgets.QPushButton("清除")
        button_clear.clicked.connect(self.clear_data)
        button_clear.setStyleSheet(button_style)
        buttons_parent_widget_layout.addWidget(button_clear, 0, 1)

        # 創建 & 設定儲存按鈕(layer 3)
        button_save = QtWidgets.QPushButton("儲存")
        button_save.clicked.connect(self.save_data)
        button_save.setStyleSheet(button_style)
        buttons_parent_widget_layout.addWidget(button_save, 0, 2)

        # 創建 & 設定下一步按鈕(layer 3)
        button_next = QtWidgets.QPushButton("下一步")
        button_next.clicked.connect(lambda: print("下一步按鈕被點擊"))
        button_next.setStyleSheet(button_style)
        buttons_parent_widget_layout.addWidget(button_next, 0, 3)

        # 將按鈕區塊(layer 3)的內容加入到 basic_infos 字典中
        self.basic_infos["button_clear"] = button_clear
        self.basic_infos["button_save"] = button_save
        self.basic_infos["button_next"] = button_next

        # 將按鈕區塊(layer 2)加入到內容區塊(layer 1)的排版
        content_layout.addWidget(buttons_parent_widget)
        # ===== 第五母區塊 - buttons =====#

    def next_button(self, function):
        self.basic_infos["button_next"].clicked.connect(function)

    def get_data(self):
        data = {}
        for key, widget in self.basic_infos.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                data[key] = widget.text()
            elif isinstance(widget, QtWidgets.QButtonGroup):
                selected_button = widget.checkedButton()
                if selected_button:
                    data[key] = selected_button.text()
                else:
                    data[key] = None
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
            self.save_path_text["save_path_input"].setText(folder_path)

    def clear_data(self):
        for key, widget in self.basic_infos.items():
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
            print(df)

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