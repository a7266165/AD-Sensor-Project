AD-Sensor-Project

# 結構樹
```
├── .gitignore
├── arduino
│   └── LED.ino
├── data
│   ├── .gitignore
│   ├── haarcascade_frontalface_default.xml
│   ├── symmetry_all_pairs.csv
│   └── XGBoost.json
├── main.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── saved_data
├── test_util
│   └── connect_arduino.py
├── ui
│   ├── pages
│   │   ├── analysis_report_window.py
│   │   ├── patient_data_form.py
│   │   └── pic_caping_window.py
│   └── styles
│       ├── analysis_report_window_style.py
│       ├── patient_data_form_style.py
│       └── pic_caping_window_style.py
└── utils
    ├── analysis_pic.py
    ├── cap_pic.py
    ├── led_controller.py
    └── predict_questionaire.py

```

# 快速啟動程式
(1) 複製專案
git clone <https://github.com/a7266165/AD-Sensor-Project.gitl>
cd AD-Sensor-Project

(2) 使用 Poetry 安裝相依套件
poetry install

(3) 啟動界面
python main.py


# 基本資料儲存格式
ID,cap_date,gender,birthday,education_years,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
ID: 患者識別碼
cap_date: 資料捕捉日期
gender: 性別
birthday: 出生日期
education_years: 教育年數
q1-q10: 問卷題目回答 (1-10題)