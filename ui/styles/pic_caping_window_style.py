# pic_caping_window_style.py - 拍攝視窗樣式設定

# 主視窗背景樣式
MAIN_WINDOW_STYLE = "background-color: rgb(248, 249, 250);"

# 標題文字樣式
TITLE_STYLE = "font-size: 24px; font-weight: bold; color: rgb(0,0,0);"

# 攝像頭顯示區域樣式
CAMERA_REGION_STYLE = "background-color: black; border-radius: 4px;"

# 按鈕樣式
BUTTON_STYLE = """
    QPushButton {
        background-color: #d54e4e;
        color: white;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #3a76d8;
    }
    QPushButton:pressed {
        background-color: #2a66c8;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #888888;
    }
"""

# 倒數計時標籤樣式
COUNTDOWN_LABEL_STYLE = "font-size: 20px;"

# 路徑標籤樣式
PATH_LABEL_STYLE = "font-size: 16px; color: gray;"
