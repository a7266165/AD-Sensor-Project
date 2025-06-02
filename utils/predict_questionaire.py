import numpy as np
import pandas as pd
from xgboost import XGBClassifier

def load_patient_data(csv_path, patient_id):
    """載入病患資料"""
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        row = df[df["ID"] == patient_id]

        if row.empty:
            raise ValueError(f"找不到病患ID: {patient_id}")

        return row
    except Exception as e:
        raise Exception(f"載入資料錯誤: {str(e)}")

def prepare_features(row):
    """準備模型特徵"""
    try:
        # 計算年齡
        cap_date = pd.to_datetime(row["cap_date"].values[0])
        birthday = pd.to_datetime(row["birthday"].values[0])
        age = (cap_date - birthday).days // 365

        # 轉換性別
        gender_str = row["gender"].values[0]
        gender_numeric = 1 if gender_str == "男" else 0

        # 教育年數
        education_years = row["education_years"].values[0]

        # 構建特徵向量
        feature_values = [age, gender_numeric, education_years] + [
            row[f"q{i}"].values[0] for i in range(1, 11)
        ]

        return np.array(feature_values).reshape(1, -1)
    except Exception as e:
        raise Exception(f"特徵準備錯誤: {str(e)}")

def predict_with_model(X, model_path):
    """使用模型進行預測"""
    try:
        model = XGBClassifier()
        model.load_model(model_path)
        y_pred = model.predict(X)
        return y_pred[0]
    except Exception as e:
        raise Exception(f"模型預測錯誤: {str(e)}")

def run_questionnaire_prediction(csv_path, patient_id, model_path):
    """執行完整的問卷預測流程"""
    try:
        # 1. 載入病患資料
        row = load_patient_data(csv_path, patient_id)

        # 2. 準備特徵
        X = prepare_features(row)

        # 3. 模型預測
        prediction = predict_with_model(X, model_path)

        return prediction
    except Exception as e:
        raise Exception(f"問卷預測流程錯誤: {str(e)}")
