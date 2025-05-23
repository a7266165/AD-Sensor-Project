import sys
from PyQt6 import QtWidgets, QtCore
# from window_setup import window_setup
import pandas as pd
import os

# 字型設定
def font_setup(font, font_size, font_weight):
    font_Set = f'font-family: "{font}"; font-size: {font_size}px; font-weight:{font_weight};'
    return font_Set

# 標籤設定
def label_setup(text, font_Set):
    label = QtWidgets.QLabel(text)
    label.setStyleSheet(f"{font_Set}")
    return label

# 輸入框設定
def entry_setup(prompt_text, font_Set):
    entry = QtWidgets.QLineEdit()
    entry.setPlaceholderText(prompt_text)  # 設定提示文字
    entry.setStyleSheet(f"{font_Set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px")  # 設定字型大小
    return entry

# 下拉選單設定
def combobox_setup(items, font_set):
    comboBox = QtWidgets.QComboBox()
    comboBox.setStyleSheet(f'{font_set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')  # 設定字型大小
    comboBox.addItems(items)
    comboBox.setCurrentIndex(0)  # 設定預設選項
    return comboBox

#===== 日歷 =====#
def photography_year_connect(date):
    text = date.toString('yyyy-MM-dd')
    text_split = text.split('-')
    photography_year = int(text_split[0])
    
    return photography_year

def birth_year_connect(date):
    text = date.toString('yyyy-MM-dd')
    text_split = text.split('-')
    birth_year = int(text_split[0])
    photography_year_connect(date)

    return birth_year

def date_setup(Form, font_Set, connect_function):
    date = QtWidgets.QDateEdit(Form)  # 建立日期調整元件
    date.setDisplayFormat('yyyy-MM-dd')  # 設定顯示格式
    date.setDate(QtCore.QDate.currentDate())
    date.setKeyboardTracking(False)
    date.setCalendarPopup(True)  # 設定為彈出式日曆
    date.setStyleSheet(f'{font_Set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')
    date.dateChanged.connect(connect_function)  # 連結日期變更事件
    

    return date

# 按鈕設定
def close_window():
    Form.close()

def clean_data():
    for entry in clear_entry_container:
        entry.clear()
    for comboBox in clear_combobox_container:
        comboBox.setCurrentIndex(0)
    for date in clear_data_container:
        date.setDate(QtCore.QDate.currentDate())

def save_data():
    # 建立一個空的 DataFrame
    df = pd.DataFrame()
    all_data = []
    # 儲存輸入框資料
    for information in all_data_container:
        if isinstance(information, QtWidgets.QLineEdit):
            all_data.append(information.text())
        elif isinstance(information, QtWidgets.QComboBox):
            all_data.append(information.currentText())
        elif isinstance(information, QtWidgets.QDateEdit):
            date_string = information.date().toString("yyyy-MM-dd")
            all_data.append(date_string)
        else:
            print(f"未知的資料類型: {type(information)}")

    print(all_data)

    # 指定儲存檔案的路徑和名稱
    save_path = 'D:\感測器專題_阿茲海默症/'

    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)

    file_exists = os.path.isfile(save_path + 'Patient_data.csv')
    print(file_exists)

    columns = all_label_container
    df = pd.DataFrame([all_data], columns= columns)

    try:
        if file_exists:
            df.to_csv(save_path + 'Patient_data.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
            print(f"資料成功儲存到 {save_path}")
            Form.close()
        else:
            df.to_csv(save_path + 'Patient_data.csv', mode='w', index=False, encoding='utf-8-sig', header=True)
            print(f"資料第一次成功儲存到 {save_path}")
            Form.close()
    except Exception as e:
        print(f"儲存資料時發生錯誤: {e}")

def button_setup(text, connect_function):
    button = QtWidgets.QPushButton(text)
    button.clicked.connect(connect_function)  # 連結按鈕點擊事件
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: rgb(255, 255, 255);
            color: rgb(0, 0, 0);
            border: 1.5px solid black;
            border-radius: 12px;
            text-align: center;
            font-family: "微軟正黑體";
            font-size: 20px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: rgb(174, 214, 241);
        }}
        QPushButton:pressed {{
            background-color: rgb(30, 144, 255);
            color: rgb(255, 255, 255);
            border: 1.5px dashed black;
            
        }}
    """)
    return button

# 建立視窗
app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
# Form, window_width, window_height = window_setup(app, Form, "個人資料")
Form.move(500, 60)  # 設定視窗位置
# print(window_width, window_height)

# 建立主垂直佈局
main_box = QtWidgets.QWidget(Form)
main_box.setStyleSheet("background-color: rgb(213, 245, 227);")
main_layout = QtWidgets.QVBoxLayout(main_box)
main_layout.setSpacing(10)

# 建立第一個子網格佈局及其容器(個人資料)
grid1_box = QtWidgets.QWidget()
grid1_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px;")
grid1_layout = QtWidgets.QGridLayout(grid1_box)
label_個人資料 = label_setup("個人資料", None)
label_個人資料.setStyleSheet("font-size: 20px; font-family: 微軟正黑體; font-weight: bold;")
grid1_layout.addWidget(label_個人資料, 0, 0)
grid1_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

main_layout.addWidget(grid1_box)


# 建立清除資料的容器
clear_entry_container = []
clear_data_container = []
clear_combobox_container = []

# 建立儲存資料的容器
# save_entry_container = []
# save_date_container = []
# save_combobox_container = []
all_label_container = []
all_data_container = []

# 建立第二個子網格佈局及其容器(基本資料)
grid2_box = QtWidgets.QWidget()
grid2_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 30px;")
grid2_layout = QtWidgets.QGridLayout(grid2_box)
grid2_layout.setSpacing(15)

font_Set = font_setup("微軟正黑體", 16, 'bold')

label_基本資料 = label_setup("基本資料", font_Set)
grid2_layout.addWidget(label_基本資料, 0, 0, 1, 4)

text = ['編號 :', '身高 :', '年齡 :', '體重 :']

for i in range(len(text)):
    row = i // 2 + 1  # 計算所在的列
    col = (i % 2) * 2  # 計算所在的欄 (0 或 2)
    label = label_setup(text[i], font_Set)
    grid2_layout.addWidget(label, row, col)
    entry = entry_setup("請輸入" + text[i].replace(" :", ""), font_Set)
    grid2_layout.addWidget(entry, row, col + 1)
    clear_entry_container.append(entry)  # 儲存輸入框的參考，為了後續clear data使用
    all_data_container.append(entry)  # 儲存輸入框的參考，為了後續save data使用
    all_label_container.append(label.text())  # 儲存標籤的參考，為了後續save data使用

sex_items = ['請選擇性別', '男', '女', '其他']
label_性別 = label_setup("性別 :", font_Set)
grid2_layout.addWidget(label_性別, 3, 0)
comboBox_性別 = combobox_setup(sex_items, font_Set)
grid2_layout.addWidget(comboBox_性別, 3, 1)
clear_combobox_container.append(comboBox_性別)  # 儲存下拉選單的參考，為了後續clear data使用
all_data_container.append(comboBox_性別)  # 儲存下拉選單的參考，為了後續save data使用
all_label_container.append(label_性別.text())  # 儲存標籤的參考，為了後續save data使用

label_生日 = label_setup("生日 :", font_Set)
grid2_layout.addWidget(label_生日, 3, 2)
entry_生日 = date_setup(Form, font_Set, birth_year_connect)
grid2_layout.addWidget(entry_生日, 3, 3)
clear_data_container.append(entry_生日)  # 儲存日期選擇器的參考，為了後續clear data使用
all_data_container.append(entry_生日)  # 儲存日期選擇器的參考，為了後續save data使用
all_label_container.append(label_生日.text())  # 儲存標籤的參考，為了後續save data使用

label_聯絡電話 = label_setup("聯絡電話 :", font_Set)
grid2_layout.addWidget(label_聯絡電話, 4, 0)
entry_聯絡電話 = entry_setup("請輸入聯絡電話:09xxxxxxxx", font_Set)
entry_聯絡電話.setMaxLength(10)  # 設定最大字元數
grid2_layout.addWidget(entry_聯絡電話, 4, 1, 1, 3)
clear_entry_container.append(entry_聯絡電話)  # 儲存輸入框的參考，為了後續clear data使用
all_data_container.append(entry_聯絡電話)  # 儲存輸入框的參考，為了後續save data使用
all_label_container.append(label_聯絡電話.text())  # 儲存標籤的參考，為了後續save data使用


main_layout.addWidget(grid2_box)

# 建立第三個子網格佈局及其容器(拍攝資訊)
grid3_box = QtWidgets.QWidget()
grid3_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 30px;")
grid3_layout = QtWidgets.QGridLayout(grid3_box)
grid3_layout.setSpacing(15)

label_拍攝資訊 = label_setup("拍攝資訊", font_Set)
grid3_layout.addWidget(label_拍攝資訊, 0, 0, 1, 4)

label_拍攝日期 = label_setup("拍攝日期 :", font_Set)
grid3_layout.addWidget(label_拍攝日期, 1, 0)
entry_拍攝日期 = date_setup(Form, font_Set, photography_year_connect)
grid3_layout.addWidget(entry_拍攝日期, 1, 1, 1, 3)
clear_data_container.append(entry_拍攝日期)  # 儲存日期選擇器的參考，為了後續clear data使用
all_data_container.append(entry_拍攝日期)  # 儲存日期選擇器的參考，為了後續save data使用
all_label_container.append(label_拍攝日期.text())  # 儲存標籤的參考，為了後續save data使用

label_拍攝地點 = label_setup("拍攝地點 :", font_Set)
grid3_layout.addWidget(label_拍攝地點, 2, 0)
entry_拍攝地點 = entry_setup("請輸入拍攝地點", font_Set)
grid3_layout.addWidget(entry_拍攝地點, 2, 1, 1, 3)
clear_entry_container.append(entry_拍攝地點)  # 儲存輸入框的參考，為了後續clear data使用
all_data_container.append(entry_拍攝地點)  # 儲存輸入框的參考，為了後續save data使用
all_label_container.append(label_拍攝地點.text())  # 儲存標籤的參考，為了後續save data使用

picture_reason_items = ['請選擇拍攝原因', '醫療檢查', '健康檢查', '其他']
label_拍攝原因 = label_setup("拍攝原因 :", font_Set)
grid3_layout.addWidget(label_拍攝原因, 3, 0)
comboBox_拍攝原因 = combobox_setup(picture_reason_items, font_Set)
grid3_layout.addWidget(comboBox_拍攝原因, 3, 1, 1, 3)
clear_combobox_container.append(comboBox_拍攝原因)  # 儲存下拉選單的參考，為了後續clear data使用
all_data_container.append(comboBox_拍攝原因)  # 儲存下拉選單的參考，為了後續save data使用
all_label_container.append(label_拍攝原因.text())  # 儲存標籤的參考，為了後續save data使用

main_layout.addWidget(grid3_box)

# 建立第四個子網格佈局及其容器(醫療資訊)
grid4_box = QtWidgets.QWidget()
grid4_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 30px;")
grid4_layout = QtWidgets.QGridLayout(grid4_box)
grid4_layout.setSpacing(15)

label_醫療資訊 = label_setup("醫療資訊", font_Set)
grid4_layout.addWidget(label_醫療資訊, 0, 0, 1, 4)
text = ['病史 :', '過敏藥物 :', '服用藥物 :', '注意事項 :']
for i in range(len(text)):
    row = i % len(text) + 1
    label = label_setup(text[i], font_Set)
    grid4_layout.addWidget(label, row, 0)
    entry = entry_setup("請輸入" + text[i].replace(" :", ""), font_Set)
    grid4_layout.addWidget(entry, row, 1, 1, 3)
    clear_entry_container.append(entry)  # 儲存輸入框的參考，為了後續clear data使用
    all_data_container.append(entry)  # 儲存輸入框的參考，為了後續save data使用
    all_label_container.append(label.text())  # 儲存標籤的參考，為了後續save data使用

main_layout.addWidget(grid4_box)

# 建立第五個子網格佈局及其容器(按鈕)
grid5_box = QtWidgets.QWidget()
grid5_layout = QtWidgets.QGridLayout(grid5_box)
grid5_layout.setSpacing(15)

button_關閉 = button_setup("關閉", close_window)

button_清除資料 = button_setup("清除資料", clean_data)

button_儲存資料 = button_setup("儲存資料", save_data)
grid5_layout.addWidget(button_關閉, 0, 0)
grid5_layout.addWidget(button_清除資料, 0, 1)
grid5_layout.addWidget(button_儲存資料, 0, 2, 1, 2)

main_layout.addWidget(grid5_box)

form_layout = QtWidgets.QVBoxLayout(Form)
form_layout.addWidget(main_box)
form_layout.setContentsMargins(0, 0, 0, 0) # 確保 Form 的佈局沒有邊距
Form.setLayout(form_layout)

Form.show()
sys.exit(app.exec())