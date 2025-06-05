import os
import cv2
import numpy as np
import pandas as pd
import zipfile
import tempfile
import shutil
from typing import Dict, List, Tuple, Optional, Union
import mediapipe as mp
import json
import xgboost as xgb
import base64

class FaceAnalysisAPI:
    """
    人臉分析API類別
    輸入：相片壓縮檔
    輸出：FaceMesh特徵點座標和不對稱性指標
    """
    
    def __init__(self, symmetry_csv_path: str = None, xgb_model_path: str = None):
        """
        初始化API
        
        Args:
            symmetry_csv_path: 對稱性配對CSV檔案路徑
            xgb_model_path: XGBoost模型檔案路徑
        """
        # 初始化MediaPipe FaceMesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.symmetry_csv_path = symmetry_csv_path
        self.xgb_model_path = xgb_model_path
        
        # 載入XGBoost模型
        self.xgb_model = None
        if xgb_model_path and os.path.exists(xgb_model_path):
            try:
                self.xgb_model = xgb.Booster()
                self.xgb_model.load_model(xgb_model_path)
            except Exception as e:
                print(f"載入XGBoost模型失敗: {e}")
        
        # 定義人臉中軸線
        self.FACEMESH_MID_LINE = [
            (10, 151), (151, 9), (9, 8), (8, 168), (168, 6),
            (6, 197), (197, 195), (195, 5), (5, 4), (4, 1),
            (1, 19), (19, 94), (94, 2),
        ]

    def analyze_from_zip(self, zip_file_path: str) -> Dict:
        """
        從壓縮檔分析人臉
        
        Args:
            zip_file_path: 壓縮檔路徑
            
        Returns:
            Dict: 包含landmarks和symmetry_metrics的結果
        """
        # 創建臨時目錄
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # 解壓縮檔案
                extracted_dir = self._extract_zip_file(zip_file_path, temp_dir)
                
                # 分析人臉
                result = self._analyze_face_from_folder(extracted_dir)
                
                return result
                
            except Exception as e:
                return {
                    "success": False,
                    "error": f"分析失敗: {str(e)}",
                    "asymmetry_classification_result": None,
                    "marked_figure": None
                }

    def analyze_from_folder(self, folder_path: str) -> Dict:
        """
        從資料夾分析人臉
        
        Args:
            folder_path: 包含相片的資料夾路徑
            
        Returns:
            Dict: 包含landmarks和symmetry_metrics的結果
        """
        return self._analyze_face_from_folder(folder_path)

    def _extract_zip_file(self, zip_file_path: str, extract_to: str) -> str:
        """解壓縮檔案"""
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # 找到包含圖片的資料夾
        for root, dirs, files in os.walk(extract_to):
            jpg_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if jpg_files:
                return root
        
        raise ValueError("壓縮檔中未找到圖片檔案")

    def _analyze_face_from_folder(self, folder_path: str) -> Dict:
        """從資料夾分析人臉"""
        try:
            # 步驟1: 選擇最正面的照片並轉正
            rotated_images = self._align_and_select_faces(folder_path)
            
            if not rotated_images:
                return {
                    "success": False,
                    "error": "未找到有效的人臉圖片",
                    "asymmetry_classification_result": None,
                    "marked_figure": None
                }
            
            # 步驟2: 提取正規化特徵點座標
            landmarks = self._extract_normalized_landmark_coordinates(rotated_images)
            
            if landmarks is None:
                return {
                    "success": False,
                    "error": "無法提取特徵點",
                    "asymmetry_classification_result": None,
                    "marked_figure": None
                }
            
            # 步驟3: 計算不對稱性指標
            symmetry_metrics = None
            asymmetry_classification = None
            if self.symmetry_csv_path:
                symmetry_metrics = self._calculate_symmetry_metrics(landmarks)
                if symmetry_metrics and self.xgb_model:
                    asymmetry_classification = self._predict_asymmetry(symmetry_metrics)
            
            # 步驟4: 生成標記圖片
            marked_figure = self._generate_marked_figure(rotated_images[0])
            
            return {
                "success": True,
                "error": None,
                "asymmetry_classification_result": asymmetry_classification,
                "marked_figure": marked_figure
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"分析過程發生錯誤: {str(e)}",
                "asymmetry_classification_result": None,
                "marked_figure": None
            }

    def _get_point(self, results, index: int, width: int, height: int) -> np.ndarray:
        """將 landmark 轉換為經過寬高縮放的二維點"""
        pt = results.multi_face_landmarks[0].landmark[index]
        return np.array([pt.x * width, pt.y * height])

    def _angle_between(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """計算兩向量之間的夾角（單位：度）"""
        return np.degrees(
            np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        )

    def _calc_intermediate_angle_sum(self, results, height: int, width: int) -> float:
        """計算中間兩個夾角的總和"""
        p1, p2, p3, p4 = [self._get_point(results, i, width, height) for i in (10, 168, 4, 2)]
        angle1 = self._angle_between(p2 - p1, p3 - p2)
        angle2 = self._angle_between(p3 - p2, p4 - p3)
        return angle1 + angle2

    def _mid_line_angle_all_points(self, results, height: int, width: int) -> float:
        """計算人臉中軸線各段的角度，並回傳平均角度"""
        angles = []
        for i, j in self.FACEMESH_MID_LINE:
            p1, p2 = self._get_point(results, i, width, height), self._get_point(results, j, width, height)
            angles.append(np.degrees(np.arctan2(p2[0] - p1[0], p2[1] - p1[1])))
        return sum(angles) / len(angles)

    def _rotate_image(self, image: np.ndarray) -> np.ndarray:
        """根據人臉中軸角度，將圖片旋轉調整至正立"""
        height, width = image.shape[:2]
        results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            return image
        
        angle = self._mid_line_angle_all_points(results, height, width)
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, -angle, 1.0)
        return cv2.warpAffine(image, M, (width, height))

    def _align_and_select_faces(self, face_pic_folder: str) -> List[np.ndarray]:
        """選取夾角總和最小的10張圖片並旋轉"""
        angle_dict = {}
        
        # 支援多種圖片格式
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        
        for file in os.listdir(face_pic_folder):
            if not file.lower().endswith(valid_extensions):
                continue
                
            path = os.path.join(face_pic_folder, file)
            image = cv2.imread(path)
            if image is None:
                continue
                
            height, width = image.shape[:2]
            results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not results.multi_face_landmarks:
                continue
                
            angle_dict[file] = self._calc_intermediate_angle_sum(results, height, width)

        if not angle_dict:
            return []

        # 選出夾角總和最小的10張圖（代表正對相機）
        selected_files = sorted(angle_dict, key=lambda x: angle_dict[x])[:10]

        # 將選取的圖片轉正
        rotated_images = []
        for file in selected_files:
            image = cv2.imread(os.path.join(face_pic_folder, file))
            if image is not None:
                rotated_image = self._rotate_image(image)
                rotated_images.append(rotated_image)
                
        return rotated_images

    def _extract_normalized_landmark_coordinates(self, rotated_face_images: List[np.ndarray]) -> Optional[np.ndarray]:
        """提取正規化的特徵點座標"""
        landmarks_all = []

        for image in rotated_face_images:
            height, width = image.shape[:2]
            results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not results.multi_face_landmarks:
                continue
                
            landmarks = results.multi_face_landmarks[0].landmark

            # 取出臉部最左邊和最上面的點
            left_x = landmarks[234].x * width
            top_y = landmarks[10].y * height
            
            pts = []
            for i in range(468):
                pt = landmarks[i]
                x = (pt.x * width) - left_x
                y = (pt.y * height) - top_y
                pts.append((x, y))
            pts = np.array(pts)

            # 依據臉部最右側點固定臉的寬度為500
            right_x = pts[454][0]
            if right_x <= 0:
                continue
                
            scale_factor = 500 / right_x
            pts = pts * scale_factor
            pts = pts.T  # 轉置成 (2, 468)
            landmarks_all.append(pts)

        if not landmarks_all:
            return None

        landmarks_all = np.array(landmarks_all)
        # 取平均
        landmarks_all = np.mean(landmarks_all, axis=0).reshape(1, 2, 468)

        # 新增z軸座標（設為0）
        z_coords = np.zeros((1, 1, 468))
        landmarks_all = np.concatenate([landmarks_all, z_coords], axis=1)

        return landmarks_all

    def _parse_idxs(self, s: str) -> List[int]:
        """解析索引字串"""
        return list(map(int, s.split(",")))

    def _line_len(self, x: Dict, y: Dict, idxs: List[int]) -> float:
        """計算線段長度"""
        i, j = idxs
        return np.hypot(x[i] - x[j], y[i] - y[j])

    def _tri_area(self, x: Dict, y: Dict, idxs: List[int]) -> float:
        """計算三角形面積"""
        i, j, k = idxs
        x1, y1 = x[i], y[i]
        x2, y2 = x[j], y[j]
        x3, y3 = x[k], y[k]
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)

    def _calculate_symmetry_metrics(self, landmarks: np.ndarray) -> Optional[Dict]:
        """計算對稱性指標"""
        if not self.symmetry_csv_path or not os.path.exists(self.symmetry_csv_path):
            return None
            
        try:
            # 讀取對稱配對資料
            df_pairs = pd.read_csv(self.symmetry_csv_path)

            # 拆分三種類型的配對
            df_pts = df_pairs[df_pairs["pair_type"].str.startswith("point")].copy()
            df_lines = df_pairs[df_pairs["pair_type"].str.startswith("line")].copy()
            df_tri = df_pairs[df_pairs["pair_type"].str.startswith("triangle")].copy()

            # 解析線段和三角形的索引
            if not df_lines.empty:
                df_lines["left_idx"] = df_lines["left"].apply(self._parse_idxs)
                df_lines["right_idx"] = df_lines["right"].apply(self._parse_idxs)
            if not df_tri.empty:
                df_tri["left_idx"] = df_tri["left"].apply(self._parse_idxs)
                df_tri["right_idx"] = df_tri["right"].apply(self._parse_idxs)

            # 從landmarks提取x, y座標
            x_coords = landmarks[0, 0, :]
            y_coords = landmarks[0, 1, :]

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
                if idx_l < 468 and idx_r < 468:
                    diff_x = abs(abs(x[idx_l] - 250) - abs(x[idx_r] - 250)) / baseline_x
                    total_pt_x += diff_x

            # 計算點對稱 Y 差值
            for _, r in df_pts.iterrows():
                idx_l = int(r["left"])
                idx_r = int(r["right"])
                if idx_l < 468 and idx_r < 468:
                    diff_y = abs(y[idx_l] - y[idx_r]) / baseline_y
                    total_pt_y += diff_y

            # 計算線段對稱差值
            for _, r in df_lines.iterrows():
                if all(idx < 468 for idx in r["left_idx"]) and all(idx < 468 for idx in r["right_idx"]):
                    ld = self._line_len(x, y, r["left_idx"])
                    rd = self._line_len(x, y, r["right_idx"])
                    if ld + rd > 0:
                        diff_line = abs(ld - rd) / (ld + rd)
                        total_line += diff_line

            # 計算三角形面積對稱差值
            for _, r in df_tri.iterrows():
                if all(idx < 468 for idx in r["left_idx"]) and all(idx < 468 for idx in r["right_idx"]):
                    la = self._tri_area(x, y, r["left_idx"])
                    ra = self._tri_area(x, y, r["right_idx"])
                    if la + ra > 0:
                        diff_tri = abs(la - ra) / (la + ra)
                        total_tri += diff_tri

            return {
                "sum_point_x_diff": float(total_pt_x),
                "sum_point_y_diff": float(total_pt_y),
                "sum_line_diff": float(total_line),
                "sum_triangle_area_diff": float(total_tri),
            }

        except Exception as e:
            print(f"計算對稱性指標錯誤: {str(e)}")
            return None

    def _predict_asymmetry(self, symmetry_metrics: Dict) -> Optional[float]:
        """
        使用XGBoost模型預測不對稱性分類結果
        
        Args:
            symmetry_metrics: 對稱性指標字典
            
        Returns:
            預測結果（機率值或分類結果）
        """
        if not self.xgb_model or not symmetry_metrics:
            return None
            
        try:
            # 準備輸入特徵
            features = [
                symmetry_metrics["sum_point_x_diff"],
                symmetry_metrics["sum_point_y_diff"], 
                symmetry_metrics["sum_line_diff"],
                symmetry_metrics["sum_triangle_area_diff"]
            ]
            
            # 轉換為XGBoost DMatrix格式
            dmatrix = xgb.DMatrix([features])
            
            # 預測
            prediction = self.xgb_model.predict(dmatrix)
            
            # 回傳預測結果（通常是機率值或分類結果）
            return float(prediction[0])
            
        except Exception as e:
            print(f"XGBoost預測錯誤: {str(e)}")
            return None

    def _generate_marked_figure(self, image: np.ndarray) -> Optional[str]:
        """
        生成帶有特徵點標記的圖片，並轉換為base64字串
        
        Args:
            image: 輸入圖片
            
        Returns:
            base64編碼的圖片字串
        """
        try:
            marked_image = self._get_face_with_landmarks_from_image(image)
            if marked_image is None:
                return None
                
            # 將圖片編碼為JPEG格式
            _, buffer = cv2.imencode('.jpg', marked_image)
            
            # 轉換為base64字串
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            print(f"生成標記圖片錯誤: {str(e)}")
            return None

    def _get_face_with_landmarks_from_image(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        從已經轉正的圖片獲取帶有特徵點標記的人臉圖片（只截取人臉部分）
        
        Args:
            image: 已經轉正的圖片
            
        Returns:
            標記了特徵點的圖片（只包含人臉部分）
        """
        height, width = image.shape[:2]
        
        # 檢測特徵點
        results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            return image
        
        # 獲取原始特徵點位置
        original_landmarks = results.multi_face_landmarks[0].landmark
        
        # 根據特定的特徵點來確定裁剪範圍
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
        
        # 計算縮放比例，使臉寬為500像素
        face_width = right_x - left_x
        if face_width <= 0:
            return image
            
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
            x = int((pt.x * width - left) * scale_factor)
            y = int((pt.y * height - top) * scale_factor)
            
            if 0 <= x < new_width and 0 <= y < new_height:
                cv2.circle(image_with_landmarks, (x, y), 2, (0, 0, 255), -1)  # 紅色點
        
        # 繪製中線
        mid_x = new_width // 2
        cv2.line(image_with_landmarks, (mid_x, 0), (mid_x, new_height), (0, 255, 255), 2)  # 黃色線
        
        # 如果有對稱性CSV，繪製線段
        if self.symmetry_csv_path and os.path.exists(self.symmetry_csv_path):
            try:
                df_pairs = pd.read_csv(self.symmetry_csv_path, encoding='utf-8-sig')
                df_lines = df_pairs[df_pairs['pair_type'].str.startswith('line')]
                
                for _, row_pair in df_lines.iterrows():
                    for side in ('left', 'right'):
                        try:
                            idx0, idx1 = map(int, row_pair[side].split(','))
                            if idx0 < 468 and idx1 < 468:
                                pt0 = original_landmarks[idx0]
                                pt1 = original_landmarks[idx1]
                                
                                x0 = int((pt0.x * width - left) * scale_factor)
                                y0 = int((pt0.y * height - top) * scale_factor)
                                x1 = int((pt1.x * width - left) * scale_factor)
                                y1 = int((pt1.y * height - top) * scale_factor)
                                
                                if (0 <= x0 < new_width and 0 <= y0 < new_height and 
                                    0 <= x1 < new_width and 0 <= y1 < new_height):
                                    cv2.line(image_with_landmarks, (x0, y0), (x1, y1), (0, 255, 0), 1)  # 綠色線
                        except:
                            continue
            except Exception as e:
                print(f"繪製線段時發生錯誤: {e}")
        
        return image_with_landmarks


# FastAPI 封裝
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    """API 回應模型"""
    success: bool
    error: Optional[str] = None
    asymmetry_classification_result: Optional[float] = None
    marked_figure: Optional[str] = None

class FaceAnalysisFastAPI:
    """FastAPI 封裝"""
    
    def __init__(self, symmetry_csv_path: str = None, xgb_model_path: str = None):
        self.app = FastAPI(
            title="人臉分析API",
            description="上傳人臉相片壓縮檔，回傳不對稱性分類結果和標記圖片",
            version="1.0.0"
        )
        self.analyzer = FaceAnalysisAPI(symmetry_csv_path, xgb_model_path)
        self.setup_routes()
        
    def setup_routes(self):
        """設定API路由"""
        
        @self.app.post("/analyze", response_model=AnalysisResponse, summary="分析人臉不對稱性")
        async def analyze_face(file: UploadFile = File(...)):
            """
            分析人臉不對稱性的API端點
            
            - **file**: 包含人臉相片的ZIP壓縮檔
            
            回傳:
            - **success**: 分析是否成功
            - **error**: 錯誤訊息（如有）
            - **asymmetry_classification_result**: XGBoost模型預測結果
            - **marked_figure**: base64編碼的標記圖片
            """
            # 檢查檔案類型
            if not file.filename.lower().endswith('.zip'):
                return AnalysisResponse(
                    success=False,
                    error="僅支援ZIP檔案",
                    asymmetry_classification_result=None,
                    marked_figure=None
                )
            
            # 檢查檔案大小（例如限制50MB）
            content = await file.read()
            if len(content) > 50 * 1024 * 1024:  # 50MB
                return AnalysisResponse(
                    success=False,
                    error="檔案大小超過50MB限制",
                    asymmetry_classification_result=None,
                    marked_figure=None
                )
            
            # 儲存上傳的檔案並分析
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                    temp_file.write(content)
                    temp_file.flush()
                    
                    # 分析人臉
                    result = self.analyzer.analyze_from_zip(temp_file.name)
                    
                    # 清理臨時檔案
                    os.unlink(temp_file.name)
                    
                    return AnalysisResponse(**result)
                    
            except Exception as e:
                return AnalysisResponse(
                    success=False,
                    error=f"處理檔案時發生錯誤: {str(e)}",
                    asymmetry_classification_result=None,
                    marked_figure=None
                )
        
        @self.app.get("/health", summary="健康檢查")
        async def health_check():
            """健康檢查端點"""
            return {
                "status": "healthy",
                "service": "Face Analysis API",
                "version": "1.0.0"
            }
        
        @self.app.get("/", summary="API資訊")
        async def root():
            """API根路徑，回傳基本資訊"""
            return {
                "message": "人臉分析API",
                "docs": "/docs",
                "health": "/health",
                "analyze": "/analyze (POST with ZIP file)"
            }
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
        """啟動API服務"""
        uvicorn.run(
            "face_analysis_api:app" if not reload else self.app,
            host=host,
            port=port,
            reload=reload
        )


# 使用範例
if __name__ == "__main__":
    # 方法1：直接使用分析器
    # analyzer = FaceAnalysisAPI("symmetry_all_pairs.csv", "xgb_face_asym_model.json")
    # result = analyzer.analyze_from_zip("face_photos.zip")
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 方法2：啟動FastAPI服務
    api_server = FaceAnalysisFastAPI("./data/symmetry_all_pairs.csv", "./data/xgb_face_asym_model.json")
    print("啟動人臉分析FastAPI服務...")
    print("API端點:")
    print("  POST /analyze - 上傳ZIP檔案進行人臉分析")
    print("  GET /health - 健康檢查")
    print("  GET / - API資訊")
    print("  GET /docs - Swagger文檔")
    print("  GET /redoc - ReDoc文檔")
    print("\n回傳格式:")
    print("  - success: 布林值，是否成功")
    print("  - error: 錯誤訊息（如有）")
    print("  - asymmetry_classification_result: XGBoost模型預測結果")
    print("  - marked_figure: base64編碼的標記圖片")
    print("\n服務將在 http://localhost:8000 啟動")
    api_server.run(reload=True)