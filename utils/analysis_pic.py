import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

FACEMESH_MID_LINE = [
    (10, 151),
    (151, 9),
    (9, 8),
    (8, 168),
    (168, 6),
    (6, 197),
    (197, 195),
    (195, 5),
    (5, 4),
    (4, 1),
    (1, 19),
    (19, 94),
    (94, 2),
]


# -----------1. 篩選相片-----------#
def get_point(results, index, width, height):
    """將 landmark 轉換為經過寬高縮放的二維點"""
    pt = results.multi_face_landmarks[0].landmark[index]
    return np.array([pt.x * width, pt.y * height])


def angle_between(v1, v2):
    """計算兩向量之間的夾角（單位：度）"""
    return np.degrees(
        np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    )


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
        p1, p2 = get_point(results, i, width, height), get_point(
            results, j, width, height
        )
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
        if not file.endswith(".jpg"):
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
    rotated_images = [
        rotate_image(os.path.join(face_pic_folder, file), face_mesh)
        for file in selected_files
    ]
    return rotated_images


# -----------2. 特徵正規化-----------#
# 將特徵點座標正規化
def extract_normalized_landmark_coordinates(rotated_face_images, face_mesh):
    """
    輸入十張已經轉正的人臉圖片，
    將每張圖片的特徵點座標正規化，
    回傳一個 numpy 陣列，形狀為 (1, 3, 468)
    其中 3 為 x, y, z 座標，468 為標點數量
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

    # 新增z軸座標（設為0）以符合(1, 3, 468)的形狀
    z_coords = np.zeros((1, 1, 468))
    landmarks_all = np.concatenate([landmarks_all, z_coords], axis=1)

    return landmarks_all


def analyze_face_landmarks(save_pic_folder, face_mesh):
    """分析臉部特徵點"""
    try:
        imgs = align_and_select_faces(save_pic_folder, face_mesh)
        if not imgs:
            return None

        landmarks = extract_normalized_landmark_coordinates(imgs, face_mesh)
        return landmarks

    except Exception as e:
        print(f"臉部特徵點分析錯誤: {str(e)}")
        return None


# -----------3. 取出特定點的座標-----------#
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
        row[f"x{p}"] = face_img_landmark[0, 0, p]
    # 取得指定點的 y 座標
    for p in specific_points:
        row[f"y{p}"] = face_img_landmark[0, 1, p]

    df = pd.DataFrame([row])
    # 依指定順序排列欄位：先 x 座標，再 y 座標
    x_cols = [f"x{p}" for p in specific_points]
    y_cols = [f"y{p}" for p in specific_points]
    df = df[x_cols + y_cols]
    return df


# -----------4. 對稱性計算-----------#
def _parse_idxs(s):
    """解析索引字串"""
    return list(map(int, s.split(",")))


def _line_len(x, y, idxs):
    """計算線段長度"""
    i, j = idxs
    return np.hypot(x[i] - x[j], y[i] - y[j])


def _tri_area(x, y, idxs):
    """計算三角形面積"""
    i, j, k = idxs
    x1, y1 = x[i], y[i]
    x2, y2 = x[j], y[j]
    x3, y3 = x[k], y[k]
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)


def calculate_symmetry_metrics(landmarks, symmetry_csv_path):
    """
    計算對稱性指標

    Args:
        landmarks: numpy array, shape (1, 3, 468)
        symmetry_csv_path: 對稱配對CSV檔案路徑

    Returns:
        dict: 包含四個對稱性指標的字典
    """
    try:
        # 讀取對稱配對資料
        df_pairs = pd.read_csv(symmetry_csv_path)

        # 拆分三種類型的配對
        df_pts = df_pairs[df_pairs["pair_type"].str.startswith("point")].copy()
        df_lines = df_pairs[df_pairs["pair_type"].str.startswith("line")].copy()
        df_tri = df_pairs[df_pairs["pair_type"].str.startswith("triangle")].copy()

        # 解析線段和三角形的索引
        df_lines["left_idx"] = df_lines["left"].apply(_parse_idxs)
        df_lines["right_idx"] = df_lines["right"].apply(_parse_idxs)
        df_tri["left_idx"] = df_tri["left"].apply(_parse_idxs)
        df_tri["right_idx"] = df_tri["right"].apply(_parse_idxs)

        # 從landmarks提取x, y座標
        # landmarks shape: (1, 3, 468) - [batch, coordinates(x,y,z), points]
        x_coords = landmarks[0, 0, :]  # 所有點的x座標
        y_coords = landmarks[0, 1, :]  # 所有點的y座標

        # 建立座標字典
        x = {i: x_coords[i] for i in range(468)}
        y = {i: y_coords[i] for i in range(468)}

        # 計算基準線
        baseline_x = abs(x[234] - x[454])
        baseline_y = abs(y[10] - y[152])

        # 避免除以零
        if baseline_x == 0:
            baseline_x = 1
        if baseline_y == 0:
            baseline_y = 1

        # 初始化累加器
        total_pt_x = 0.0
        total_pt_y = 0.0
        total_line = 0.0
        total_tri = 0.0

        # 計算點對稱 X 差值
        for _, r in df_pts.iterrows():
            idx_l = int(r["left"])
            idx_r = int(r["right"])
            if idx_l < 468 and idx_r < 468:  # 確保索引有效
                diff_x = abs(abs(x[idx_l] - 250) - abs(x[idx_r] - 250)) / baseline_x
                total_pt_x += diff_x

        # 計算點對稱 Y 差值
        for _, r in df_pts.iterrows():
            idx_l = int(r["left"])
            idx_r = int(r["right"])
            if idx_l < 468 and idx_r < 468:  # 確保索引有效
                diff_y = abs(y[idx_l] - y[idx_r]) / baseline_y
                total_pt_y += diff_y

        # 計算線段對稱差值
        for _, r in df_lines.iterrows():
            # 檢查所有索引是否有效
            if all(idx < 468 for idx in r["left_idx"]) and all(
                idx < 468 for idx in r["right_idx"]
            ):
                ld = _line_len(x, y, r["left_idx"])
                rd = _line_len(x, y, r["right_idx"])
                if ld + rd > 0:  # 避免除以零
                    diff_line = abs(ld - rd) / (ld + rd)
                    total_line += diff_line

        # 計算三角形面積對稱差值
        for _, r in df_tri.iterrows():
            # 檢查所有索引是否有效
            if all(idx < 468 for idx in r["left_idx"]) and all(
                idx < 468 for idx in r["right_idx"]
            ):
                la = _tri_area(x, y, r["left_idx"])
                ra = _tri_area(x, y, r["right_idx"])
                if la + ra > 0:  # 避免除以零
                    diff_tri = abs(la - ra) / (la + ra)
                    total_tri += diff_tri

        return {
            "sum_point_x_diff": total_pt_x,
            "sum_point_y_diff": total_pt_y,
            "sum_line_diff": total_line,
            "sum_triangle_area_diff": total_tri,
        }

    except Exception as e:
        print(f"計算對稱性指標錯誤: {str(e)}")
        return None


# -----------5. 繪圖-----------#
def get_original_face_with_landmarks(
    face_pic_folder, face_mesh, landmarks, symmetry_csv_path=None
):
    """
    獲取帶有特徵點標記的原始人臉圖片（只截取人臉部分）

    Args:
        face_pic_folder: 人臉圖片資料夾
        face_mesh: MediaPipe FaceMesh 物件
        landmarks: 正規化後的特徵點座標 (1, 3, 468)
        symmetry_csv_path: 對稱性CSV檔案路徑

    Returns:
        標記了特徵點的圖片（只包含人臉部分）
    """
    # 選擇一張最正面的圖片
    angle_dict = {}
    for file in os.listdir(face_pic_folder):
        if not file.endswith(".jpg"):
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

    if not angle_dict:
        return None

    # 選擇最正面的圖片
    best_file = min(angle_dict, key=angle_dict.get)
    best_path = os.path.join(face_pic_folder, best_file)

    # 載入並旋轉圖片
    image = rotate_image(best_path, face_mesh)
    height, width = image.shape[:2]

    # 重新檢測旋轉後圖片的特徵點
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return image

    # 獲取原始特徵點位置
    original_landmarks = results.multi_face_landmarks[0].landmark

    # 計算人臉邊界框
    x_coords = [landmark.x * width for landmark in original_landmarks]
    y_coords = [landmark.y * height for landmark in original_landmarks]

    # 根據特定的特徵點來確定裁剪範圍（與正規化時使用的點一致）
    left_x = original_landmarks[234].x * width
    right_x = original_landmarks[454].x * width
    top_y = original_landmarks[10].y * height
    bottom_y = original_landmarks[152].y * height

    # 添加一些邊距
    margin = 5
    left = max(0, int(left_x - margin))
    right = min(width, int(right_x + margin))
    top = max(0, int(top_y - margin))
    bottom = min(height, int(bottom_y + margin))

    # 裁剪圖片
    cropped_image = image[top:bottom, left:right]
    cropped_height, cropped_width = cropped_image.shape[:2]

    # 計算縮放比例，使臉寬為500像素（與正規化時一致）
    face_width = right_x - left_x
    scale_factor = 500 / face_width

    # 調整裁剪後圖片的大小
    new_width = int(cropped_width * scale_factor)
    new_height = int(cropped_height * scale_factor)
    resized_image = cv2.resize(cropped_image, (new_width, new_height))

    # 在調整大小後的圖片上繪製特徵點和線段
    image_with_landmarks = resized_image.copy()

    # 繪製特徵點
    for i in range(468):
        pt = original_landmarks[i]
        # 轉換座標到裁剪並縮放後的圖片座標系
        x = int((pt.x * width - left) * scale_factor)
        y = int((pt.y * height - top) * scale_factor)

        # 確保點在圖片範圍內
        if 0 <= x < new_width and 0 <= y < new_height:
            cv2.circle(image_with_landmarks, (x, y), 2, (0, 0, 255), -1)  # 紅色點

    # 繪製中線（應該在圖片中央）
    mid_x = new_width // 2
    cv2.line(
        image_with_landmarks, (mid_x, 0), (mid_x, new_height), (0, 255, 255), 2
    )  # 黃色線

    # 如果有對稱性CSV，繪製線段
    if symmetry_csv_path:
        try:
            df_pairs = pd.read_csv(symmetry_csv_path, encoding="utf-8-sig")
            df_lines = df_pairs[df_pairs["pair_type"].str.startswith("line")]

            for _, row_pair in df_lines.iterrows():
                for side in ("left", "right"):
                    try:
                        idx0, idx1 = map(int, row_pair[side].split(","))
                        if idx0 < 468 and idx1 < 468:
                            pt0 = original_landmarks[idx0]
                            pt1 = original_landmarks[idx1]

                            # 轉換座標
                            x0 = int((pt0.x * width - left) * scale_factor)
                            y0 = int((pt0.y * height - top) * scale_factor)
                            x1 = int((pt1.x * width - left) * scale_factor)
                            y1 = int((pt1.y * height - top) * scale_factor)

                            # 確保線段的兩個端點都在圖片範圍內
                            if (
                                0 <= x0 < new_width
                                and 0 <= y0 < new_height
                                and 0 <= x1 < new_width
                                and 0 <= y1 < new_height
                            ):
                                cv2.line(
                                    image_with_landmarks,
                                    (x0, y0),
                                    (x1, y1),
                                    (0, 255, 0),
                                    1,
                                )  # 綠色線
                    except:
                        continue
        except Exception as e:
            print(f"繪製線段時發生錯誤: {e}")

    return image_with_landmarks


def plot_face_landmarks_with_lines(landmarks, symmetry_csv_path, ax, face_image=None):
    """
    在指定的 matplotlib axes 上繪製臉部特徵點和線段

    Args:
        landmarks: 特徵點座標 (1, 3, 468)
        symmetry_csv_path: 對稱性CSV檔案路徑
        ax: matplotlib axes 物件
        face_image: 人臉圖片 (可選)
    """
    if landmarks is None or len(landmarks) == 0:
        ax.text(
            0.5, 0.5, "無法取得特徵點", ha="center", va="center", transform=ax.transAxes
        )
        return

    # 如果有人臉圖片，直接顯示帶有標記的圖片
    if face_image is not None:
        # 將BGR轉換為RGB以正確顯示顏色
        ax.imshow(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
        ax.set_title("Face Landmarks Analysis")
    else:
        # 沒有圖片時使用原始方式繪製
        x = landmarks[0, 0, :]  # x座標
        y = landmarks[0, 1, :]  # y座標

        # 繪製中線
        ax.axvline(x=250, color="r", linestyle="--", label="midline", alpha=0.7)

        # 繪製特徵點
        ax.scatter(x, y, s=1, c="red", alpha=0.5)

        # 如果有對稱性CSV檔案，繪製線段
        if symmetry_csv_path:
            try:
                df_pairs = pd.read_csv(symmetry_csv_path, encoding="utf-8-sig")
                df_lines = df_pairs[df_pairs["pair_type"].str.startswith("line")]

                # 準備線段數據
                line_segments = []
                for _, row_pair in df_lines.iterrows():
                    for side in ("left", "right"):
                        try:
                            idx0, idx1 = map(int, row_pair[side].split(","))
                            if idx0 < len(x) and idx1 < len(x):
                                line_segments.append(
                                    ((x[idx0], y[idx0]), (x[idx1], y[idx1]))
                                )
                        except:
                            continue

                # 繪製線段
                if line_segments:
                    lc = LineCollection(
                        line_segments, linewidths=1, colors="lime", alpha=0.8
                    )
                    ax.add_collection(lc)

            except Exception as e:
                print(f"警告：讀取對稱性CSV檔案時發生錯誤: {e}")

        ax.set_xlim(x.min() - 20, x.max() + 20)
        ax.set_ylim(y.max() + 20, y.min() - 20)
        ax.set_title("Face Landmarks with Line Segments")
        ax.legend()

    # 隱藏坐標軸
    ax.set_xticks([])
    ax.set_yticks([])


def setup_analysis_plot(
    canvas, landmarks, face_mesh, symmetry_csv_path, face_pic_folder=None
):
    """
    設定分析圖表

    Args:
        canvas: matplotlib canvas 物件
        landmarks: 特徵點座標 (1, 3, 468) 或 None
        symmetry_csv_path: 對稱性CSV檔案路徑
        face_pic_folder: 人臉圖片資料夾路徑 (可選)
    """
    fig = canvas.figure
    fig.clear()

    # 創建單一子圖
    ax = fig.add_subplot(1, 1, 1)

    # 檢查landmarks是否有效
    if landmarks is not None and len(landmarks) > 0:
        face_image = None

        # 如果提供了圖片資料夾，嘗試獲取帶有標記的人臉圖片
        if face_pic_folder and os.path.exists(face_pic_folder):
            # 獲取帶有特徵點標記的圖片
            face_image = get_original_face_with_landmarks(
                face_pic_folder, face_mesh, landmarks, symmetry_csv_path
            )

        # 繪製特徵點和線段
        plot_face_landmarks_with_lines(landmarks, symmetry_csv_path, ax, face_image)
    else:
        # 顯示無數據訊息
        ax.text(
            0.5,
            0.5,
            "無可用的影像數據進行分析",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=16,
        )
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("分析結果")

    # 調整布局
    fig.tight_layout()
    canvas.draw()
