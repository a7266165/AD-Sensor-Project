import sys
import os

# 路徑設定
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

import numpy as np
import pandas as pd
from PyQt6 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils import analysis_pic, predict_questionaire
import mediapipe as mp

# 導入樣式設定
from ui.styles.analysis_report_window_style import (
    TITLE_STYLE,
    RESULT_LABEL_STYLE,
    REANALYZE_BUTTON_STYLE,
    CLOSE_BUTTON_STYLE,
    MAIN_WINDOW_STYLE,
    SYMMETRY_GROUP_STYLE,
    SYMMETRY_LABEL_STYLE,
    STATUS_MESSAGE_STYLE,
    ERROR_MESSAGE_STYLE,
)


class AnalysisReportWindow(QtWidgets.QFrame):
    """分析報告視窗"""

    def __init__(
        self, save_parent_folder, patient_id, csv_path, symmetry_csv_path, model_path
    ):
        super().__init__()
        self.save_parent_folder = save_parent_folder
        self.patient_id = patient_id
        self.save_pic_folder = os.path.join(save_parent_folder, patient_id)
        self.csv_path = csv_path
        self.symmetry_csv_path = symmetry_csv_path
        self.model_path = model_path
        self._landmarks_cache = None  # 測試用，之後要移除

        self._init_window()
        self._init_ui()

    def _init_window(self):
        """初始化視窗設定"""
        self.setWindowTitle("分析結果")
        self.resize(900, 900)  # 增加高度以容納新的數值顯示
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def _init_ui(self):
        """初始化使用者介面"""
        layout = QtWidgets.QVBoxLayout(self)  # layer 0

        # ===== 第一母區塊 - title =====
        title_label = QtWidgets.QLabel("分析報告")  # layer 1
        title_label.setStyleSheet(TITLE_STYLE)
        layout.addWidget(title_label)

        # ===== 第二母區塊 - predict result =====
        self.result_label = QtWidgets.QLabel("預測結果: --")  # layer 1
        self.result_label.setStyleSheet(RESULT_LABEL_STYLE)
        layout.addWidget(self.result_label)

        # ===== 第三母區塊 - symmetry analysis =====
        symmetry_group = QtWidgets.QGroupBox("對稱性分析結果")  # layer 1
        symmetry_group.setStyleSheet(SYMMETRY_GROUP_STYLE)
        symmetry_layout = QtWidgets.QGridLayout()

        # 建立四個標籤來顯示對稱性數值
        self.symmetry_labels = {
            "x": QtWidgets.QLabel("X軸點對稱差值總和: --"),
            "y": QtWidgets.QLabel("Y軸點對稱差值總和: --"),
            "line": QtWidgets.QLabel("線段對稱差值總和: --"),
            "triangle": QtWidgets.QLabel("三角形面積對稱差值總和: --"),
        }

        # 將標籤添加到網格佈局中
        row = 0
        for key, label in self.symmetry_labels.items():
            label.setStyleSheet(SYMMETRY_LABEL_STYLE)
            symmetry_layout.addWidget(label, row // 2, row % 2)
            row += 1

        symmetry_group.setLayout(symmetry_layout)
        layout.addWidget(symmetry_group)

        # ===== 第四母區塊 - 繪製標點後的人臉 =====
        self.canvas = FigureCanvas(plt.Figure(figsize=(10, 8)))
        layout.addWidget(self.canvas)

        # ===== 第五母區塊 - 按鈕區域 =====
        button_layout = QtWidgets.QHBoxLayout()

        # 重新分析按鈕
        btn_reanalyze = QtWidgets.QPushButton("重新分析")  # layer 1
        btn_reanalyze.clicked.connect(self.run_analysis)
        btn_reanalyze.setStyleSheet(REANALYZE_BUTTON_STYLE)
        button_layout.addWidget(btn_reanalyze)

        # 關閉按鈕
        btn_close = QtWidgets.QPushButton("關閉應用")  # layer 1
        btn_close.clicked.connect(QtWidgets.QApplication.quit)
        btn_close.setStyleSheet(CLOSE_BUTTON_STYLE)
        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

    def _update_symmetry_display(self, metrics):
        """更新對稱性數值顯示"""
        if metrics:
            self.symmetry_labels["x"].setText(
                f"X軸點對稱差值總和: {metrics['sum_point_x_diff']:.4f}"
            )
            self.symmetry_labels["y"].setText(
                f"Y軸點對稱差值總和: {metrics['sum_point_y_diff']:.4f}"
            )
            self.symmetry_labels["line"].setText(
                f"線段對稱差值總和: {metrics['sum_line_diff']:.4f}"
            )
            self.symmetry_labels["triangle"].setText(
                f"三角形面積對稱差值總和: {metrics['sum_triangle_area_diff']:.4f}"
            )
        else:
            for label in self.symmetry_labels.values():
                label.setText(label.text().split(":")[0] + ": 計算失敗")

    def run_analysis(self):
        """執行完整分析流程"""
        try:
            # 1. 問卷預測
            prediction = predict_questionaire.run_questionnaire_prediction(
                self.csv_path, self.patient_id, self.model_path
            )
            self.result_label.setText(f"模型預測結果: {prediction}")
        except Exception as e:
            self.result_label.setText(f"問卷預測錯誤: {str(e)}")

        # 2. 臉部特徵點分析
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8,
        )

        landmarks = analysis_pic.analyze_face_landmarks(self.save_pic_folder, face_mesh)

        # 測試用，之後要移除
        self._landmarks_cache = landmarks
        print(
            f"Landmarks shape: {landmarks.shape if landmarks is not None else 'None'}"
        )

        # 3. 計算對稱性指標
        if landmarks is not None:
            symmetry_metrics = analysis_pic.calculate_symmetry_metrics(
                landmarks, self.symmetry_csv_path
            )
            self._update_symmetry_display(symmetry_metrics)

        # 4. 繪製分析圖表
        analysis_pic.setup_analysis_plot(
            self.canvas,
            landmarks,
            face_mesh,
            self.symmetry_csv_path,
            self.save_pic_folder,
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 測試參數
    save_parent_folder = r"C:\Users\a1234\Desktop\AD-Sensor-Project\saved_data"
    patient_id = "P2-5_no_rotated"
    csv_path = os.path.join(save_parent_folder, "AD_patient_data.csv")
    model_path = r"C:\Users\a1234\Desktop\AD-Sensor-Project\data\XGBoost.json"
    symmetry_csv_path = (
        r"C:\Users\a1234\Desktop\AD-Sensor-Project\data\symmetry_all_pairs.csv"
    )

    window = AnalysisReportWindow(
        save_parent_folder, patient_id, csv_path, symmetry_csv_path, model_path
    )

    # 執行分析並保存landmarks到CSV
    window.run_analysis()

    # 如果有landmarks資料，將其保存為CSV檔案
    if hasattr(window, "_landmarks_cache") and window._landmarks_cache is not None:
        landmarks = window._landmarks_cache

        # 準備資料字典
        data_dict = {}

        # 提取x, y, z座標
        x_coords = landmarks[0, 0, :]  # 所有點的x座標
        y_coords = landmarks[0, 1, :]  # 所有點的y座標
        z_coords = landmarks[0, 2, :]  # 所有點的z座標

        # 將座標加入字典
        for i in range(468):
            data_dict[f"x{i}"] = x_coords[i]
            data_dict[f"y{i}"] = y_coords[i]
            data_dict[f"z{i}"] = z_coords[i]

        # 建立DataFrame
        df_landmarks = pd.DataFrame([data_dict])

        # 保存到CSV檔案
        output_csv_path = os.path.join(
            save_parent_folder, f"{patient_id}_landmarks_3d.csv"
        )
        df_landmarks.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        print(f"三維座標已保存到: {output_csv_path}")

        # 另外保存一個更易讀的格式（每個點一行）
        readable_data = []
        for i in range(468):
            readable_data.append(
                {"point_index": i, "x": x_coords[i], "y": y_coords[i], "z": z_coords[i]}
            )

        df_readable = pd.DataFrame(readable_data)
        readable_csv_path = os.path.join(
            save_parent_folder, f"{patient_id}_landmarks_readable.csv"
        )
        df_readable.to_csv(readable_csv_path, index=False, encoding="utf-8-sig")
        print(f"易讀格式座標已保存到: {readable_csv_path}")
    else:
        print("警告：無法取得landmarks資料")

    window.show()
    sys.exit(app.exec())
