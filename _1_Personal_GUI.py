import sys
import os
from PyQt6 import QtWidgets, QtCore
import pandas as pd
from widger_helper import label_setup, entry_setup, combobox_setup, date_setup, button_setup

class InfoWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.widgets = {}
        self.save_path_text = {}
        self.ui()

    def ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        
        #===== Create first gird layout =====#
        grid1_box = QtWidgets.QWidget()
        grid1_box.setStyleSheet("")
        grid1_box.setFixedHeight(40)
        self.grid1_layout = QtWidgets.QGridLayout(grid1_box)
        label_personal_data = label_setup("表單", None)
        label_personal_data.setStyleSheet("font-size: 24px; font-family: 微軟正黑體; font-weight: bold; border: 0px;")
        self.grid1_layout.addWidget(label_personal_data, 0, 0)
        self.grid1_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        #===== Finish =====#

        #===== Create second gird layout =====#
        grid2_box = QtWidgets.QWidget()
        grid2_box.setStyleSheet("border: 0px;")
        grid2_box.setFixedHeight(40)
        self.grid2_layout = QtWidgets.QGridLayout(grid2_box)
        label_base_information = label_setup("基本資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_base_information, 0, 0, 1, 4)
        #===== Finish =====#
        
        #===== Create third gird layout =====#
        grid3_box = QtWidgets.QWidget()
        grid3_box.setStyleSheet("border: 0px;")
        self.grid3_layout = QtWidgets.QGridLayout(grid3_box)
        self.grid3_layout.setSpacing(15)
        label_ID = label_setup("編號 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_ID, 0, 0)
        entry_ID = entry_setup("請輸入編號", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(entry_ID, 0, 1)
        self.widgets['ID'] = entry_ID

        label_gender = label_setup("性別 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_gender, 1, 0)
        gender = combobox_setup(["請選擇性別","男", "女"], "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(gender, 1, 1)
        self.widgets['gender'] = gender

        label_photography_year = label_setup("拍攝日期 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_photography_year, 0, 2)
        capture_pic_date = date_setup(self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(capture_pic_date, 0, 3)
        self.widgets['capture_pic_date'] = capture_pic_date

        label_birthday = label_setup("生日 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_birthday, 1, 2)
        birthday = date_setup(self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(birthday, 1, 3)
        self.widgets['birthday'] = birthday
        #===== Finish =====#

        #===== Create combine second and third gird layout =====#
        combine_layout2_layout3_box = QtWidgets.QWidget()
        combine_layout2_layout3_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout2_layout3 = QtWidgets.QVBoxLayout(combine_layout2_layout3_box)
        self.combine_layout2_layout3.addWidget(grid2_box)
        self.combine_layout2_layout3.addWidget(grid3_box)
        #==== Finish ====#


        #===== Create fourth gird layout =====#
        grid4_box = QtWidgets.QWidget()
        grid4_box.setStyleSheet("border: 0px;")
        self.grid4_layout = QtWidgets.QGridLayout(grid4_box)
        self.grid4_layout.setSpacing(15)

        label_photography_information = label_setup("6QDS答案", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_photography_information, 0, 0, 1, 4)
        self.widgets['label_photography_information'] = label_photography_information
        #==== Finish ====#

        #===== Create fifth gird layout =====#
        grid5_box = QtWidgets.QWidget()
        grid5_box.setStyleSheet("border: 0px;")
        self.grid5_layout = QtWidgets.QGridLayout(grid5_box)
        self.grid5_layout.setSpacing(15)
        q1 = label_setup("q1 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q1, 0, 0)
        entry_q1 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q1, 0, 1)
        self.widgets['q1'] = entry_q1
        q2 = label_setup("q2 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q2, 0, 2)
        entry_q2 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q2, 0, 3)
        self.widgets['q2'] = entry_q2
        q3 = label_setup("q3 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q3, 0, 4)
        entry_q3 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q3, 0, 5)
        self.widgets['q3'] = entry_q3
        q4 = label_setup("q4 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q4, 0, 6)
        entry_q4 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q4, 0, 7)
        self.widgets['q4'] = entry_q4
        q5 = label_setup("q5 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q5, 0, 8)
        entry_q5 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q5, 0, 9)
        self.widgets['q5'] = entry_q5
        q6 = label_setup("q6 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q6, 1, 0)
        entry_q6 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q6, 1, 1)
        self.widgets['q6'] = entry_q6        
        q7 = label_setup("q7 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q7, 1, 2)
        entry_q7 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q7, 1, 3)
        self.widgets['q7'] = entry_q7
        q8 = label_setup("q8 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q8, 1, 4)
        entry_q8 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q8, 1, 5)
        self.widgets['q8'] = entry_q8
        q9 = label_setup("q9 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q9, 1, 6)
        entry_q9 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q9, 1, 7)
        self.widgets['q9'] = entry_q9
        q10 = label_setup("q10 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(q10, 1, 8)
        entry_q10 = entry_setup("評分", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_q10, 1, 9)
        self.widgets['q10'] = entry_q10
        #===== Finish =====#

        #===== Create combine fourth and fifth gird layout =====#
        combine_layout4_layout5_box = QtWidgets.QWidget()
        combine_layout4_layout5_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout4_layout5 = QtWidgets.QVBoxLayout(combine_layout4_layout5_box)
        self.combine_layout4_layout5.addWidget(grid4_box)
        self.combine_layout4_layout5.addWidget(grid5_box)
        #==== Finish ====#
        
        #===== Create combine eighth gird layout =====#
        grid8_layout_box = QtWidgets.QWidget()
        grid8_layout_box.setStyleSheet("border: 0px;")
        grid8_layout_box.setFixedHeight(40)
        self.grid8_layout = QtWidgets.QGridLayout(grid8_layout_box)
        label_save_path = label_setup("儲存路徑 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid8_layout.addWidget(label_save_path, 0, 0)
        #==== Finish =====#

        #===== Create ninth gird layout =====#
        grid9_layout_box = QtWidgets.QWidget()
        grid9_layout_box.setStyleSheet("border: 0px;")
        self.grid9_layout = QtWidgets.QGridLayout(grid9_layout_box)
        entry_save_path = entry_setup("", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;") 
        entry_save_path.setReadOnly(True)
        self.grid9_layout.addWidget(entry_save_path, 1, 0, 1, 4)
        self.save_path_text['entry_save_path'] = entry_save_path
        #==== Finish =====#

        #===== Create combine eighth and ninth gird layout =====#
        combine_layout8_layout9_box = QtWidgets.QWidget()
        combine_layout8_layout9_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout8_layout9 = QtWidgets.QVBoxLayout(combine_layout8_layout9_box)
        self.combine_layout8_layout9.addWidget(grid8_layout_box)
        self.combine_layout8_layout9.addWidget(grid9_layout_box)
        #==== Finish ====#

        #===== Create tenth grid layout =====#
        grid10_box = QtWidgets.QWidget()
        # grid5_box.setFixedHeight(60)
        self.grid10_layout = QtWidgets.QGridLayout(grid10_box)
        self.grid10_layout.setSpacing(15)

        button_save_folder = button_setup("選擇儲存資料夾", self.open_save_folder)
        self.grid10_layout.addWidget(button_save_folder, 0, 0, 1, 2)


        button_clear = button_setup("清除", self.clear_data)
        self.grid10_layout.addWidget(button_clear, 0, 3)
        self.widgets['button_clear'] = button_clear

        button_save = button_setup("儲存", self.save_data)
        self.grid10_layout.addWidget(button_save, 1, 0, 1, 2)
        self.widgets['button_save'] = button_save

        button_next = button_setup("下一步", lambda: print("下一步按鈕被點擊"))
        self.grid10_layout.addWidget(button_next, 1, 3)
        self.widgets['button_next'] = button_next
        #==== Finish =====#    

        #===== Create scroll area =====#
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        scroll_area.setStyleSheet("border: 0px;")
        # scroll_area.setFixedHeight(1000)
        #===== Finish =====#

        #==== Finally, add the grid layout to the main layout ====#
        self.main_layout.addWidget(grid1_box)
        content_layout.addWidget(grid1_box)
        self.main_layout.addWidget(combine_layout2_layout3_box)
        content_layout.addWidget(combine_layout2_layout3_box)
        self.main_layout.addWidget(combine_layout4_layout5_box)
        content_layout.addWidget(combine_layout4_layout5_box)
        self.main_layout.addWidget(combine_layout8_layout9_box)
        content_layout.addWidget(combine_layout8_layout9_box)
        self.main_layout.addWidget(grid10_box)
        content_layout.addWidget(grid10_box)
        self.main_layout.addWidget(scroll_area)
        #===== Finish =====#
    
    def next_button(self, function):
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
    
    def open_save_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if folder_path:
            print(f"選擇的儲存資料夾: {folder_path}")
            self.save_path_text['save_path'] = folder_path
            self.save_path_text['entry_save_path'].setText(folder_path)

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

        save_path = self.save_path_text['save_path']
        file_exists = os.path.isfile(save_path + '/AD_patient_data.csv')

        if file_exists is True:
            df.to_csv(save_path + '/AD_patient_data.csv', mode='a', header=False, index=False, encoding='utf-8-sig')
            print(f'檔案接續儲存在:{save_path}AD_patient_data.csv')
            
        else:
            df.to_csv(save_path + '/AD_patient_data.csv', mode='w', header=True, index=False, encoding='utf-8-sig')
            print(f'檔案第一次儲存在:{save_path}AD_patient_data.csv')
    #===== Finish =====#

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    info_window = InfoWindow()
    info_window.setFixedSize(800, 1000)
    info_window.show()
    sys.exit(app.exec())