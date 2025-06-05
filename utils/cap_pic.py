import cv2
import numpy as np
import pyrealsense2 as rs

class RealSenseCamera(rs.pipeline):
    """
    繼承自 rs.pipeline，封裝 RealSense 顏色與深度流。
    支援相機物理旋轉（橫擺）的處理。
    - __init__: 啟動前設定 color + depth 解析度與更新率
    - start/stop: 啟/停 管線
    - get_frame: 回傳校正後的 (color_bgr, depth_map) 兩張影像
    """
    def __init__(self, width=848, height=480, fps=60, physically_rotated=False):
        super().__init__()
        cfg = rs.config()
        
        # 保持原始的相機解析度設定，不交換寬高
        # 因為相機硬體本身的感應器解析度是固定的
        cfg.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
        cfg.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
        
        self._cfg = cfg
        self._physically_rotated = physically_rotated

    def start(self):
        super().start(self._cfg)

    def stop(self):
        super().stop()

    def get_frame(self):
        """
        回傳校正後的影像：
        - color: BGR numpy 陣列（已校正方向）
        - depth: 深度值(毫米)的 numpy 陣列（已校正方向）
        若任一影像擷取失敗，回傳 (None, None)
        """
        frames = self.wait_for_frames()
        c = frames.get_color_frame()
        d = frames.get_depth_frame()
        if not c or not d:
            return None, None
            
        color = np.asanyarray(c.get_data())
        depth = np.asanyarray(d.get_data())
        
        # 如果相機物理旋轉了，需要同步旋轉兩個影像來校正
        if self._physically_rotated:
            color = cv2.rotate(color, cv2.ROTATE_90_CLOCKWISE)
            depth = cv2.rotate(depth, cv2.ROTATE_90_CLOCKWISE)
            
        return color, depth

def detect_face_distance(face_cascade, color_img, depth_img, cx, cy, square_size):
    """
    範例自 user 提供:
    - 偵測最大人臉、計算平均距離
    - 若人臉中心落在中央方框內且距離適中，方框用紅色；否則綠色
    回傳 have_face(bool)
    """
    have_face = False
    gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
        scaleFactor=1.03, minNeighbors=7, minSize=(100, 100))
    if len(faces) > 1:
        # 選最大人臉
        faces = [max(faces, key=lambda f: f[2]*f[3])]
    for (x, y, w, h) in faces:
        # 臉中心
        x_cent, y_cent = x + w//2, y + h//2
        # 深度 ROI (米)
        roi = depth_img[y:y+h, x:x+w] / 1000
        mask = (roi>0.1) & (roi<1)
        vals = roi[mask]
        ave = float(np.mean(vals)) if vals.size>0 else 0
        # 判斷顏色
        color = (0,255,0)
        if 0.35 <= ave <= 0.5 and \
           cx-square_size < x_cent < cx+square_size and \
           cy-square_size < y_cent < cy+square_size:
            color = (0,0,255)
            have_face = True
        # 繪製臉框與文字
        cv2.rectangle(color_img, (x,y), (x+w,y+h), color, 2)
        cv2.putText(color_img,
            f"Dist:{ave:.2f}m",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return have_face

def process_frame(color, depth, face_cascade, box_size=80):
    """
    對校正後的色彩影像做加工：
    1. 中央畫綠色方框
    2. 偵測人臉並標示距離（紅/綠框）
    注意：不再需要旋轉，因為影像已經在相機層面校正過了
    """
    marked_frame = color.copy()
    
    h, w = marked_frame.shape[:2]
    cx, cy = w//2, h//2
    half = box_size
    
    # 中央對齊方框
    cv2.rectangle(
        marked_frame,
        (cx-half, cy-half),
        (cx+half, cy+half),
        (0,255,0), 2
    )
    
    # 偵測與標示人臉距離（使用已校正的深度影像）
    detect_face_distance(face_cascade, marked_frame, depth, cx, cy, box_size)
    
    return marked_frame, color

def get_frames(cam, face_cascade):
    """主程式：載入 xml、擷取影像並呼叫 process_frame 顯示。"""
    while True:
        color, depth = cam.get_frame()
        if color is None:
            continue
        processed_frame, origin_frame = process_frame(color, depth, face_cascade, box_size=80)
        return processed_frame, origin_frame

# 測試用
if __name__ == "__main__":
    # 載入 Haar cascade xml
    xml_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(xml_path)

    # 告訴相機類別：相機已經物理旋轉了（橫擺）
    cam = RealSenseCamera(width=848, height=480, fps=60, physically_rotated=True)
    cam.start()
    
    try:
        while True:
            color, depth = cam.get_frame()  # 這裡已經是校正後的影像了
            if color is None:
                continue
                
            out, _ = process_frame(color, depth, face_cascade, box_size=80)
            cv2.imshow("Face & Distance", out)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.stop()
        cv2.destroyAllWindows()