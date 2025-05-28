import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import os
import numpy as np
import pandas as pd
from PyQt6 import QtWidgets
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils import analysis_pic
import mediapipe as mp

class AnalysisReportWindow(QtWidgets.QFrame):
    def __init__(self, save_parent_folder, patient_id, csv_path, symmetry_csv_path, model_path):
        super().__init__()
        self.save_parent_folder = save_parent_folder
        self.patient_id = patient_id
        self.save_pic_folder = os.path.join(save_parent_folder, patient_id)
        self.csv_path = csv_path
        self.symmetry_csv_path = symmetry_csv_path
        self.model_path = model_path
        self.setWindowTitle("分析結果")
        self.resize(900, 800)
        self.ui()

    def ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        # 顯示模型預測結果
        self.result_label = QtWidgets.QLabel("預測結果: --")
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.result_label)
        # 放置圖表畫布
        self.canvas = FigureCanvas(plt.Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)
        # 關閉按鈕
        btn_close = QtWidgets.QPushButton("關閉應用")
        btn_close.clicked.connect(QtWidgets.QApplication.quit)
        layout.addWidget(btn_close)

    def run_analysis(self):
        # 1. 讀取 CSV，篩選該 ID 的問卷資料
        df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
        row = df[df['ID'] == self.patient_id]
        if row.empty:
            self.result_label.setText("找不到對應資料")
            return

        # 計算年齡 (cap_date - birthday)
        cap_date = pd.to_datetime(row['cap_date'].values[0])
        birthday = pd.to_datetime(row['birthday'].values[0])
        age = (cap_date - birthday).days // 365

        # 轉換性別 (男=1, 女=0)
        gender_str = row['gender'].values[0]
        gender_numeric = 1 if gender_str == '男' else 0

        # 教育年數
        education_years = row['education_years'].values[0]

        # 構建特徵向量，請確保與模型訓練時的特徵順序一致
        feature_values = [age, gender_numeric, education_years] + [row[f'q{i}'].values[0] for i in range(1, 11)]
        X = np.array(feature_values).reshape(1, -1)

        # 2. 載入並預測
        model = XGBClassifier()
        model.load_model(self.model_path)
        y_pred = model.predict(X)
        self.result_label.setText(f"模型預測: {y_pred[0]}")

        # 3. 非對稱性分析: 取拍攝資料夾內所有相片
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        imgs = analysis_pic.align_and_select_faces(self.save_pic_folder, face_mesh)

        print(f"找到 {len(imgs)} 張圖片進行分析")
        landmarks = analysis_pic.extract_normalized_landmark_coordinates(imgs, face_mesh)

        # 4. 繪製 2×2 視覺化圖表到 Matplotlib 畫布
        fig = self.canvas.figure
        fig.clear()
        axes = fig.subplots(2, 2)
        x, y = landmarks[0][0], landmarks[0][1]
        # (0,0): 原始 scatter
        ax = axes[0, 0]
        ax.scatter(x, y, s=5)
        ax.set_title('landmarks')

        # (0,1): scatter + midline
        ax = axes[0, 1]
        ax.axvline(x=250, linestyle='--')
        ax.scatter(x, y, s=5)
        ax.set_title('landmarks + midline')
        # (1,0) CSV 定義的相鄰線段
        if self.symmetry_csv_path:
            df_pairs = pd.read_csv(self.symmetry_csv_path, encoding='utf-8-sig')
            df_lines = df_pairs[df_pairs['pair_type'].str.startswith('line')]
            from matplotlib.collections import LineCollection
            line_segments = []
            for _, row_pair in df_lines.iterrows():
                for side in ('left', 'right'):
                    idx0, idx1 = map(int, row_pair[side].split(','))
                    line_segments.append(((x[idx0], y[idx0]), (x[idx1], y[idx1])))
            ax = axes[1, 0]
            ax.axvline(x=250, color='r', linestyle='--', label='midline')
            lc = LineCollection(line_segments, linewidths=1)
            ax.add_collection(lc)
            ax.set_xlim(x.min() - 0.05, x.max() + 0.05)
            ax.set_ylim(y.max() + 0.05, y.min() - 0.05)
            ax.set_title('line segments')
            ax.legend()
        
        # (1,1) CSV 定義的三點面片
        if self.symmetry_csv_path:
            df_tris = pd.read_csv(self.symmetry_csv_path, encoding='utf-8-sig')
            df_tris = df_tris[df_tris['pair_type'].str.startswith('triangle')]
            from matplotlib.collections import PolyCollection
            tri_polys = []
            for _, row_pair in df_tris.iterrows():
                for side in ('left', 'right'):
                    idxs = list(map(int, row_pair[side].split(',')))
                    tri_polys.append([(x[i], y[i]) for i in idxs])
            ax = axes[1, 1]
            ax.axvline(x=250, color='r', linestyle='--', label='midline')
            pc = PolyCollection(tri_polys, linewidths=0.5, alpha=0.3, edgecolors='k')
            ax.add_collection(pc)
            ax.set_xlim(x.min() - 0.05, x.max() + 0.05)
            ax.set_ylim(y.max() + 0.05, y.min() - 0.05)
            ax.set_title('triangles')
            ax.legend()

        # 隱藏坐標軸並反轉
        for ax in axes.flatten():
            ax.set_xticks([])
            ax.set_yticks([])
        for ax in [axes[0, 0], axes[0, 1]]:
            ax.invert_yaxis()
        fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    save_parent_folder = r'C:\Users\4080\Desktop\python\AD-Sensor-Project\saved_data' # 替換為實際路徑
    patient_id = "P2"  # 替換為實際病人ID
    csv_path = os.path.join(save_parent_folder, "AD_patient_data.csv")
    model_path = r"C:\Users\4080\Desktop\python\AD-Sensor-Project\data\XGBoost.json"  # 替換為實際模型路徑
    symmetry_csv_path = r'C:\Users\4080\Desktop\python\AD-Sensor-Project\data\symmetry_all_pairs.csv'
    window = AnalysisReportWindow(save_parent_folder, patient_id, csv_path, symmetry_csv_path, model_path)
    window.run_analysis()
    window.show()
    sys.exit(app.exec())