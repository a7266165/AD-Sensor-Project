import sys
from PyQt6 import QtWidgets, QtCore
import pandas as pd
from widger_helper import label_setup, entry_setup, combobox_setup, date_setup, button_setup
# 主視窗



class FirstWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('個人資料')
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.widgets = {}
        self.ui()

    def ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(10)
        
        #===== Create first gird layout =====#
        grid1_box = QtWidgets.QWidget()
        grid1_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 1px solid black;")
        grid1_box.setFixedHeight(40)
        self.grid1_layout = QtWidgets.QGridLayout(grid1_box)

        label_personal_data = label_setup("個人資料", None)
        label_personal_data.setStyleSheet("font-size: 20px; font-family: 微軟正黑體; font-weight: bold; border: 0px;")
        self.grid1_layout.addWidget(label_personal_data, 0, 0)
        self.grid1_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.widgets['label_personal_data'] = label_personal_data
        #===== Finish =====#


        #===== Create second gird layout =====#
        grid2_box = QtWidgets.QWidget()
        grid2_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 1px solid black;")
        self.grid2_layout = QtWidgets.QGridLayout(grid2_box)
        

        label_base_information = label_setup("基本資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_base_information, 0, 0, 1, 4)
        self.grid2_layout.setSpacing(15)
        self.widgets['label_base_information'] = label_base_information
        
        label_ID = label_setup("編號 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_ID, 1, 0)
        entry_ID = entry_setup("請輸入編號", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(entry_ID, 1, 1)
        self.widgets['entry_ID'] = entry_ID

        label_height = label_setup("身高 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_height, 1, 2)
        entry_height = entry_setup("請輸入身高", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(entry_height, 1, 3)
        self.widgets['entry_height'] = entry_height
        
        label_age = label_setup("年齡 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_age, 2, 0)
        entry_age = entry_setup("請輸入年齡", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(entry_age, 2, 1)
        self.widgets['entry_age'] = entry_age

        label_weight = label_setup("體重 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_weight, 2, 2)
        entry_weight = entry_setup("請輸入體重", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(entry_weight, 2, 3)
        self.widgets['entry_weight'] = entry_weight

        label_gender = label_setup("性別 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_gender, 3, 0)
        combobox_gender = combobox_setup(["請選擇性別","男", "女"], "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(combobox_gender, 3, 1)
        self.widgets['combobox_gender'] = combobox_gender

        label_birthday = label_setup("生日 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_birthday, 3, 2)
        calender_birthday = date_setup(self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(calender_birthday, 3, 3)
        self.widgets['calender_birthday'] = calender_birthday

        label_contact_number = label_setup("聯絡電話 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_contact_number, 4, 0)
        entry_contact_number = entry_setup("請輸入聯絡電話:09xxxxxxxx", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        entry_contact_number.setMaxLength(10)
        self.grid2_layout.addWidget(entry_contact_number, 4, 1, 1, 3)
        self.widgets['entry_contact_number'] = entry_contact_number
        #===== Finish =====#

        #===== Create third gird layout =====#
        grid3_box = QtWidgets.QWidget()
        grid3_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 1px solid black;")
        self.grid3_layout = QtWidgets.QGridLayout(grid3_box)
        self.grid3_layout.setSpacing(15)

        label_photography_information = label_setup("拍攝資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_photography_information, 0, 0, 1, 4)
        self.widgets['label_photography_information'] = label_photography_information

        label_photography_year = label_setup("拍攝年份 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_photography_year, 1, 0)
        calender_photography_year = date_setup(self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(calender_photography_year, 1, 1, 1, 3)
        self.widgets['calender_photography_year'] = calender_photography_year

        label_photography_site = label_setup("拍攝地點 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_photography_site, 2, 0)
        entry_photography_site = entry_setup("請輸入拍攝地點", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(entry_photography_site, 2, 1, 1, 3)
        self.widgets['entry_photography_site'] = entry_photography_site

        label_photography_reason = label_setup("拍攝原因 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_photography_reason, 3, 0)
        combobox_photography_reason = combobox_setup(["請選擇拍攝原因", "醫療檢查", "健康檢查", "其他"], "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(combobox_photography_reason, 3, 1, 1, 3)
        self.widgets['combobox_photography_reason'] = combobox_photography_reason
        #===== Finish =====#

        #===== Create forth gird layout =====#
        grid4_box = QtWidgets.QWidget()
        grid4_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 1px solid black;")
        self.grid4_layout = QtWidgets.QGridLayout(grid4_box)
        self.grid4_layout.setSpacing(15)

        label_medical_information = label_setup("醫療資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_medical_information, 0, 0, 1, 4)
        self.widgets['label_medical_information'] = label_medical_information

        label_medical_history = label_setup("病史 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_medical_history, 1, 0)
        entry_medical_history = entry_setup("請輸入病史", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(entry_medical_history, 1, 1, 1, 3)
        self.widgets['entry_medical_history'] = entry_medical_history

        label_allergic_medications = label_setup("過敏藥物 : :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_allergic_medications, 2, 0)
        entry_medication_allergic_medications = entry_setup("請輸入過敏藥物", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(entry_medication_allergic_medications, 2, 1, 1, 3)
        self.widgets['entry_medication_allergic_medications'] = entry_medication_allergic_medications

        label_mideication_taken = label_setup("服用藥物 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_mideication_taken, 3, 0)
        entry_medication_taken = entry_setup("請輸入服用藥物", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(entry_medication_taken, 3, 1, 1, 3)
        self.widgets['entry_medication_taken'] = entry_medication_taken

        label_caution = label_setup("注意事項 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_caution, 4, 0)
        entry_caution = entry_setup("請輸入注意事項", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(entry_caution, 4, 1, 1, 3)
        self.widgets['entry_caution'] = entry_caution
        #===== Finish =====#

        #===== Create fivth grid layout =====#
        grid5_box = QtWidgets.QWidget()
        grid5_box.setFixedHeight(60)
        self.grid5_layout = QtWidgets.QGridLayout(grid5_box)
        self.grid5_layout.setSpacing(15)

        button_clear = button_setup("清除", self.clear_data)
        self.grid5_layout.addWidget(button_clear, 0, 0)
        self.widgets['button_clear'] = button_clear

        button_save = button_setup("儲存", self.save_data)
        self.grid5_layout.addWidget(button_save, 0, 1, 1, 2)
        self.widgets['button_save'] = button_save

        button_next = button_setup("下一步", lambda: print("下一步按鈕被點擊"))
        self.grid5_layout.addWidget(button_next, 0, 3)
        self.widgets['button_next'] = button_next
    
        # Finally, add the grid layout to the main layout
        self.main_layout.addWidget(grid1_box)
        self.main_layout.addWidget(grid2_box)
        self.main_layout.addWidget(grid3_box)
        self.main_layout.addWidget(grid4_box)
        self.main_layout.addWidget(grid5_box)
    
    def connect_next_button(self, function):
        self.widgets['button_next'].clicked.connect(function)

    def get_data(self):
        data = {}
        for key, widget in self.widgets.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                data[key] = widget.text()
            elif isinstance(widget, QtWidgets.QComboBox):
                data[key] = widget.currentText()
            elif isinstance(widget, QtWidgets.QDateEdit):
                data[key] = widget.date().toString('yyyy-MM-dd')
            else:
                continue
        return data
    
    def save_data(self):
        data = self.get_data()
        df = pd.DataFrame([data])
        df.to_csv('data.csv', mode='a', header=False, index=False)
        print("Data saved:", data)

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
    

    def show(self):
        self.setLayout(self.main_layout)
        super().show()  



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    first_window = FirstWindow()
    first_window.show()
    sys.exit(app.exec())