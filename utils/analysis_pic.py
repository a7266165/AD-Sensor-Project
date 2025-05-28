import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FACEMESH_MID_LINE = [(10, 151), (151, 9), (9, 8), (8, 168), 
                    (168, 6), (6, 197), (197, 195), (195, 5), 
                    (5, 4), (4, 1), (1, 19), (19, 94), (94, 2)]

#-----------1. 篩選相片-----------#

def get_point(results, index, width, height):
    """將 landmark 轉換為經過寬高縮放的二維點"""
    pt = results.multi_face_landmarks[0].landmark[index]
    return np.array([pt.x * width, pt.y * height])

def angle_between(v1, v2):
    """計算兩向量之間的夾角（單位：度）"""
    return np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))

def calc_intermediate_angle_sum(results, height, width):
    """
    使用點 10, 168, 4, 2 分別代表鼻梁上方、鼻梁、鼻尖與人中，
    計算中間兩個夾角的總和
    """
    p1, p2, p3, p4 = [get_point(results, i, width, height) for i in (10, 168, 4, 2)]
    angle1 = angle_between(p2 - p1, p3 - p2)
    angle2 = angle_between(p3 - p2, p4 - p3)
    return angle1 + angle2

def mid_line_angle_all_points(results, height, width):
    """
    計算人臉中軸線各段的角度，並回傳平均角度
    """
    angles = []
    for i, j in FACEMESH_MID_LINE:
        p1, p2 = get_point(results, i, width, height), get_point(results, j, width, height)
        # 利用 arctan2 直接計算角度，結果會介於 -180 到 180 度之間
        angles.append(np.degrees(np.arctan2(p2[0] - p1[0], p2[1] - p1[1])))
    return sum(angles) / len(angles)

def rotate_image(face_img_path, face_mesh):
    """
    根據人臉中軸角度，將圖片旋轉調整至正立
    """
    image = cv2.imread(face_img_path)
    height, width = image.shape[:2]
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    angle = mid_line_angle_all_points(results, height, width)
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    return cv2.warpAffine(image, M, (width, height))

def align_and_select_faces(face_pic_folder, face_mesh):
    """
    遍歷資料夾中所有 jpg 圖片，選取夾角總和最小的 10 張（較正面），
    並將它們依據中軸角度進行旋轉
    """
    angle_dict = {}
    for file in os.listdir(face_pic_folder):
        if not file.endswith('.jpg'):
            continue
        path = os.path.join(face_pic_folder, file)
        image = cv2.imread(path)
        if image is None:
            continue
        height, width = image.shape[:2]
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            continue
        angle_dict[file] = calc_intermediate_angle_sum(results, height, width)
    
    # 選出夾角總和最小的 10 張圖（代表正對相機）
    selected_files = sorted(angle_dict, key=lambda x: angle_dict[x])[:10]
    
    # 將選取的圖片轉正並回傳轉正後的圖片列表
    rotated_images = [rotate_image(os.path.join(face_pic_folder, file), face_mesh) 
                      for file in selected_files]
    return rotated_images

#-----------2. 特徵正規化-----------#

# 將特徵點座標正規化
def extract_normalized_landmark_coordinates(rotated_face_images, face_mesh):
    """
    輸入十張已經轉正的人臉圖片，
    將每張圖片的特徵點座標正規化，
    回傳一個 numpy 陣列，形狀為 (N, 3, 468)
    其中 N 為圖片數量（預期為 10），3 為 x, y, z 座標，468 為標點數量
    """
    landmarks_all = []
    
    for image in rotated_face_images:
        height, width = image.shape[:2]
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            continue  # 若未偵測到臉部，跳過此圖片
        landmarks = results.multi_face_landmarks[0].landmark
        
        # 取出臉部最左邊和最上面的點，用以做座標平移
        left_x = landmarks[234].x * width
        top_y = landmarks[10].y * height
        pts = []
        for i in range(468):
            pt = landmarks[i]
            x = (pt.x * width) - left_x
            y = (pt.y * height) - top_y
            pts.append((x, y))
        pts = np.array(pts)  # shape (468, 2)

        # 依據臉部最右側點固定臉的寬度為 500
        right_x = pts[454][0]
        scale_factor = 500 / right_x
        pts = pts * scale_factor  # 進行縮放
        pts = pts.T  # 轉置成 (2, 468)，每一列分別為 x, y, z 座標
        landmarks_all.append(pts)
    
    landmarks_all = np.array(landmarks_all)  # 最終 shape 為 (N, 2, 468)
    # 將landmarks_all取平均，變成(1, 2, 468)
    landmarks_all = np.mean(landmarks_all, axis=0).reshape(1, 2, 468)

    return landmarks_all

#-----------3. 取出特定點的座標-----------#

def get_specific_landmark_coords(face_img_landmark, specific_points):
    """
    取出特定特徵點的座標，並以 DataFrame 回傳（僅取 x 與 y 軸）
    輸入:
        face_img_landmark: numpy 陣列，形狀 (1, 3, 468)
                           其中 3 分別代表 x, y, z，但此函數只使用 x 與 y 軸
        specific_points: list, 指定要取出的 landmark 索引
    輸出:
        DataFrame, 欄位依序為 x{p} (依 specific_points 順序),
                   y{p} (依 specific_points 順序)
    """
    row = {}
    # 取得指定點的 x 座標
    for p in specific_points:
        row[f'x{p}'] = face_img_landmark[0, 0, p]
    # 取得指定點的 y 座標
    for p in specific_points:
        row[f'y{p}'] = face_img_landmark[0, 1, p]
    
    df = pd.DataFrame([row])
    # 依指定順序排列欄位：先 x 座標，再 y 座標
    x_cols = [f'x{p}' for p in specific_points]
    y_cols = [f'y{p}' for p in specific_points]
    df = df[x_cols + y_cols]
    return df

#-----------4. 計算差值-----------#

def calculate_difference(left_point, right_point, power_num):
    """
    計算左右對稱特徵點在 x 與 y 軸上的差值（取差值的 power 次方），並回傳差值 DataFrame，
    不包含 image_name 資料。
    
    輸入:
        left_point: DataFrame，欄位依序為 x 座標與 y 座標 (例如 x1, x2, ..., y1, y2, ...)
        right_point: DataFrame，欄位格式與 left_point 相同
        power_num: 指數次方的數值
    輸出:
        diff_cubic: DataFrame，包含左右對稱特徵點在 x 與 y 軸上的差值的 power 次方
    """
    num_pairs = len(left_point.columns) // 2  # 此時左側欄位數為 num_pairs, 右側欄位數同理（x 與 y 各有一組）
    # 建立欄位名稱
    columns_x = [f'x_pair_{i+1}' for i in range(num_pairs)]
    columns_y = [f'y_pair_{i+1}' for i in range(num_pairs)]
    
    diff_cubic_x = pd.DataFrame(columns=columns_x)
    diff_cubic_y = pd.DataFrame(columns=columns_y)
    
    for i in range(num_pairs):
        left_x = left_point.iloc[:, i]
        right_x = right_point.iloc[:, i]
        left_y = left_point.iloc[:, i + num_pairs]
        right_y = right_point.iloc[:, i + num_pairs]

        # 計算左右對稱點到中軸 (x = 250) 的距離差
        x_diff_values = abs(abs(250 - left_x) - abs(250 - right_x))
        # 計算左右對稱點在 y 軸的距離差
        y_diff_values = abs(abs(left_y) - abs(right_y))
        
        diff_cubic_x[columns_x[i]] = x_diff_values ** power_num
        diff_cubic_y[columns_y[i]] = y_diff_values ** power_num

    diff_cubic = pd.concat([diff_cubic_x, diff_cubic_y], axis=1)

    return diff_cubic

#-----------5. 繪圖-----------#


#-----------法一 z-score-----------#

def load_stats_df(eye_stats_path, face_oval_stats_path, mouth_stats_path, nose_stats_path):
    """
    讀取各部位的平均與標準差 DataFrame
    """
    eye_stats_df = pd.read_csv(eye_stats_path, index_col='image_name')
    face_oval_stats_df = pd.read_csv(face_oval_stats_path, index_col='image_name')
    mouth_stats_df = pd.read_csv(mouth_stats_path, index_col='image_name')
    nose_stats_df = pd.read_csv(nose_stats_path, index_col='image_name')
    return eye_stats_df, face_oval_stats_df, mouth_stats_df, nose_stats_df

def calculate_z_score(diffs, stats_df):
    """
    計算 z-score
    """
    common_columns = diffs.columns.intersection(stats_df.columns)
    z_score_df = (diffs[common_columns] - stats_df.loc['Average', common_columns]) / stats_df.loc['Standard Deviation', common_columns]
    return z_score_df

def get_color_from_z(z, threshold=0.25):
    """
    根據 z-score 計算顏色 (RGB，數值介於 0~1)，並以藍色到紅色的線性漸變表示：
      - 當 z 為 0 時，回傳黑色 (0, 0, 0)
      - 當 z 大於等於 threshold (預設 3) 時，回傳紅色 (1, 0, 0)
      - 當 z 小於等於 -threshold (預設 3) 時，回傳藍色 (0, 0, 1)
      - 介於 -threshold 與 threshold 之間時，依絕對值做線性內插

    參數：
      z: 單一 z-score 值
      threshold: z-score 的臨界值（預設為 3）
    回傳：
      顏色 tuple (r, g, b)，數值介於 0~1
    """
    if z >= 0:
        factor = min(z / threshold, 1.0)
        # 由黑色 (0,0,0) 逐漸轉變為紅色 (1,0,0)
        return (factor, 0.0, 0.0)
    else:
        factor = min(abs(z) / threshold, 1.0)
        # 由黑色 (0,0,0) 逐漸轉變為藍色 (0,0,1)
        return (0.0, 0.0, factor)


def draw_multi_parts_asymmetry_subplots(parts, max_abs_z=3):
    """
    在同一張圖中建立兩個子圖，分別以 X 與 Y 的 z-score 著色，
    並同時呈現多個部位的不對稱性。
    
    每個部位的資料格式為 (part_name, left_df, right_df, z_score_df)
      - left_df: 左側座標 DataFrame，形狀 [1 x N] (前二分之一為 x 座標，後二分之一為 y 座標)
      - right_df: 右側座標 DataFrame，形狀 [1 x N]
      - z_score_df: z-score DataFrame，形狀 [1 x N] (前二分之一為 x 的 z-score，後二分之一為 y 的 z-score)
    
    子圖1：以 X 的 z-score 著色，並在 x = 250 加垂直虛線  
    子圖2：以 Y 的 z-score 著色  
    圖表固定 x 軸範圍 0～500，y 軸範圍 0～700，且反轉 y 軸 (原點位於左上方)
    """
    # 建立圖表 (1x2) 固定尺寸
    fig, axs = plt.subplots(1, 2, figsize=(10, 6))
    
    # 針對每個部位依序繪製
    for part_name, left_df, right_df, z_score_df in parts:
        # 取得左右座標 (展平成 N 個數值)
        left_coords = left_df.values.flatten()
        right_coords = right_df.values.flatten()

        # 取得每個部位的座標數量
        n = len(left_coords) // 2  # 每個部位的座標數量

        # 前二分之一為 x 座標，後二分之一為 y 座標
        left_x, left_y = left_coords[:n], left_coords[n:]
        right_x, right_y = right_coords[:n], right_coords[n:]
        
        # 取得 z-score (前二分之一為 x 的 z-score，後二分之一為 y 的 z-score)
        z_scores = z_score_df.values.flatten()
        z_x = z_scores[:n]
        z_y = z_scores[n:]
        
        # 計算各點顏色
        colors_x = [get_color_from_z(z, max_abs_z) for z in z_x]
        colors_y = [get_color_from_z(z, max_abs_z) for z in z_y]
        
        # 在子圖1 (X z-score 著色) 繪製左右座標
        axs[0].scatter(left_x, left_y, s=50, c=colors_x, marker='o', label=f'Left')
        axs[0].scatter(right_x, right_y, s=50, c=colors_x, marker='x', label=f'Right')
        
        # 在子圖2 (Y z-score 著色) 繪製左右座標
        axs[1].scatter(left_x, left_y, s=50, c=colors_y, marker='o', label=f'Left')
        axs[1].scatter(right_x, right_y, s=50, c=colors_y, marker='x', label=f'Right')
        
        # 設定子圖1：標題、軸範圍、垂直虛線及反轉 y 軸
        axs[0].set_title("Asymmetry of X-axis")
        axs[0].set_xlim(0, 500)
        axs[0].set_ylim(0, 700)
        axs[0].axvline(x=250, color='k', linestyle='--')
        axs[0].invert_yaxis()
        
        # 設定子圖2：標題、軸範圍及反轉 y 軸
        axs[1].set_title("Asymmetry of Y-axis")
        axs[1].set_xlim(0, 500)
        axs[1].set_ylim(0, 700)
        axs[1].invert_yaxis()
    
    # 隱藏兩個子圖的坐標刻度
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal', adjustable='box')
    
    # 去除重複的圖例項目（可依需要調整）
    handles0, labels0 = axs[0].get_legend_handles_labels()
    by_label0 = dict(zip(labels0, handles0))
    axs[0].legend(by_label0.values(), by_label0.keys())
    
    handles1, labels1 = axs[1].get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    axs[1].legend(by_label1.values(), by_label1.keys())
    
    plt.tight_layout()
    plt.show()

#-----------法二 差值-----------#

def get_color_from_diff(diff, max_diff=25):
    """
    根據差值計算顏色 (RGB，數值介於 0~1)：
      - 當 diff == 0 時，顏色為藍色 (0, 0, 1)
      - 當 diff >= max_diff (預設 25) 時，顏色為純紅 (1, 0, 0)
      - 中間值則從藍色逐漸轉變為紅色 (紅分量從 0 漸變到 1，藍分量則由 1 漸變到 0)
      
    參數：
      diff: 單一差值
      max_diff: 差值對應至紅色飽和的最大值 (預設 25)
    回傳：
      顏色 tuple (r, g, b)，數值介於 0~1
    """
    factor = min(diff / max_diff, 1.0)
    # 從藍色 (0,0,1) 漸變到 純紅 (1,0,0)
    return (factor, 0.0, 1.0 - factor)



def draw_multi_parts_asymmetry_subplots(parts, max_diff=25):
    """
    在同一張圖中建立兩個子圖，分別以 X 與 Y 的差值著色，
    並同時呈現多個部位的不對稱性。
    
    每個部位的資料格式為 (part_name, left_df, right_df, diff_df)
      - left_df: 左側座標 DataFrame，形狀 [1 x N] (前二分之一為 x 座標，後二分之一為 y 座標)
      - right_df: 右側座標 DataFrame，形狀 [1 x N]
      - diff_df: 差值 DataFrame，形狀 [1 x N] (前二分之一為 x 的差值，後二分之一為 y 的差值)
    
    子圖1：以 X 的差值著色，並在 x = 250 加垂直虛線  
    子圖2：以 Y 的差值著色  
    圖表固定 x 軸範圍 0～500，y 軸範圍 0～700，且反轉 y 軸 (原點位於左上方)
    """
    # 建立圖表 (1x2) 固定尺寸
    fig, axs = plt.subplots(1, 2, figsize=(10, 6))
    
    # 針對每個部位依序繪製
    for part_name, left_df, right_df, diff_df in parts:
        # 取得左右座標 (展平成 N 個數值)
        left_coords = left_df.values.flatten()
        right_coords = right_df.values.flatten()

        # 取得每個部位的座標數量 (假設前半為 x, 後半為 y)
        n = len(left_coords) // 2

        # 前二分之一為 x 座標，後二分之一為 y 座標
        left_x, left_y = left_coords[:n], left_coords[n:]
        right_x, right_y = right_coords[:n], right_coords[n:]
        
        # 取得差值 (前二分之一為 x 的差值，後二分之一為 y 的差值)
        diff_values = diff_df.values.flatten()
        diff_x = diff_values[:n]
        diff_y = diff_values[n:]
        
        # 計算各點顏色 (僅從白色漸變到紅色)
        colors_x = [get_color_from_diff(diff, max_diff = 50) for diff in diff_x]
        colors_y = [get_color_from_diff(diff, max_diff = 15) for diff in diff_y]
        
        # 在子圖1 (X 差值著色) 繪製左右座標
        axs[0].scatter(left_x, left_y, s=50, c=colors_x, marker='o', label=f'Left')
        axs[0].scatter(right_x, right_y, s=50, c=colors_x, marker='x', label=f'Right')
        
        # 在子圖2 (Y 差值著色) 繪製左右座標
        axs[1].scatter(left_x, left_y, s=50, c=colors_y, marker='o', label=f'Left')
        axs[1].scatter(right_x, right_y, s=50, c=colors_y, marker='x', label=f'Right')
    
    # 設定子圖1：標題、軸範圍、垂直虛線及反轉 y 軸
    axs[0].set_title("Asymmetry of X-axis (Difference)")
    axs[0].set_xlim(0, 500)
    axs[0].set_ylim(0, 700)
    axs[0].axvline(x=250, color='k', linestyle='--')
    axs[0].invert_yaxis()
    
    # 設定子圖2：標題、軸範圍及反轉 y 軸
    axs[1].set_title("Asymmetry of Y-axis (Difference)")
    axs[1].set_xlim(0, 500)
    axs[1].set_ylim(0, 700)
    axs[1].invert_yaxis()
    
    # 隱藏兩個子圖的坐標刻度
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal', adjustable='box')
    
    # 去除重複的圖例項目
    handles0, labels0 = axs[0].get_legend_handles_labels()
    by_label0 = dict(zip(labels0, handles0))
    axs[0].legend(by_label0.values(), by_label0.keys())
    
    handles1, labels1 = axs[1].get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    axs[1].legend(by_label1.values(), by_label1.keys())
    
    plt.tight_layout()
    plt.show()