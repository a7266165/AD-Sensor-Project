# import cv2
# import numpy as np
# import pyrealsense2 as rs

# class RealSenseCamera:
#     def __init__(self, width=848, height=480, fps=60):
#         self.pipeline = rs.pipeline()
#         self.config = rs.config()
        
#         self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)

#     def reset(self, width=848, height=480, fps=60):
#         self.stop()
#         self.__init__(width, height, fps)

#     def start(self):
#         self.pipeline.start(self.config)

#     def stop(self):
#         self.pipeline.stop()

#     def get_frame(self):
#         frames = self.pipeline.wait_for_frames()
#         color_frame = frames.get_color_frame()
#         if not color_frame:
#             return None
#         frame = np.asanyarray(color_frame.get_data())

#          # 順時針 90°
#         frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

#         # 繪製需對齊的正方型
#         x_center = int(frame.shape[1] / 2)
#         y_center = int(frame.shape[0] / 2)
#         square_size = 80
#         cv2.rectangle(frame, (x_center-square_size, y_center-square_size), (x_center+square_size, y_center+square_size), (0, 255, 0), 2)

#         return frame

# class CameraDevice:
#     def __init__(self, camera_type="RealSense"):
#         self.camera_types = ["RealSense"]        
#         self.camera_devices = [RealSenseCamera()]
#         self.camera_type = camera_type
#         self.camera = self.camera_devices[self.camera_types.index(camera_type)]
#         self.camera.start()

#     def switch_camera(self, camera_type):
#         if camera_type not in self.camera_types:
#             raise ValueError(f"Invalid camera type: {camera_type}")
#         self.camera.stop()
#         self.camera_type = camera_type
#         self.camera = self.camera_devices[self.camera_types.index(camera_type)]
#         self.camera.start()

#     def start(self):
#         self.camera.start()

#     def stop(self):
#         self.camera.stop()

#     def get_frame(self):
#         return self.camera.get_frame()

#     def release(self):
#         self.camera.release()

# # class VideoRecorder:
# #     def __init__(self, width=848, height=480, fps=60):
# #         self.width = width
# #         self.height = height
# #         self.fps = fps
# #         self.writer = None
# #         self.is_recording = False
# #         self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# #         self.duration_count = 0

# #     def set_config(self, filename, width=848, height=480, fps=60, duration=None):
# #         self.filename = filename
# #         self.fps = fps
# #         self.width = width
# #         self.height = height
# #         self.duration = duration * fps if duration else None

# #     def start(self):
# #         self.writer = cv2.VideoWriter(
# #             self.filename, self.fourcc, self.fps, (self.width, self.height)
# #         )
# #         self.is_recording = True
# #         self.duration_count = 0

# #     def stop(self):
# #         self.writer.release()
# #         self.is_recording = False

# #     def record_frame(self, frame):
# #         if frame is None:
# #             raise ValueError("Frame is None.")
# #         if self.duration is None or self.duration_count >= self.duration:
# #             self.stop()
# #             return
# #         self.writer.write(frame)
# #         self.duration_count += 1

# if __name__ == "__main__":
#     camera = CameraDevice(camera_type="RealSense")  # Change to "Webcam" for webcam
#     # video_recorder = VideoRecorder()
#     # video_recorder.set_config(filename="output.mp4", width=848, height=480, fps=60, duration=3)  # Set the desired configuration
#     # print(video_recorder.is_recording)

#     cam_idx = 0
#     while True:
#         frame = camera.get_frame()
#         if frame is None:
#             break

#         # Display the frame
#         cv2.imshow("demo", frame)
#         # if video_recorder.is_recording:
#         #     # Record the frame
#         #     video_recorder.record_frame(frame)
            
#         key = cv2.waitKey(1) & 0xFF
#         # Break the loop on 'q' key press
#         if key == ord('q'):
#             break

#         # if key == ord('s'):
#         #     video_recorder.start()

#     camera.stop()
#     cv2.destroyAllWindows()

import cv2
import numpy as np
import pyrealsense2 as rs

class RealSenseCamera:
    """
    RealSense 顏色流攝影機封裝。
    - __init__：設定解析度與更新率，但不自動啟動管線
    - start()：啟動影像管線
    - stop()：停止管線
    - get_frame()：擷取並回傳處理後影格
    - release()：釋放資源（同 stop）
    """
    def __init__(self, width=848, height=480, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self._started = False

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(
            rs.stream.color,
            self.width,
            self.height,
            rs.format.bgr8,
            self.fps
        )

    def start(self):
        """啟動 RealSense 影像管線。"""
        if not self._started:
            self.pipeline.start(self.config)
            self._started = True

    def stop(self):
        """停止 RealSense 影像管線。"""
        if self._started:
            self.pipeline.stop()
            self._started = False

    def get_frame(self):
        """
        取得一張影格，順時針旋轉 90°，並於中心畫 80×80 綠色方框。
        若讀不到影格，回傳 None。
        """
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return None

        frame = np.asanyarray(color_frame.get_data())
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        size = 80
        cv2.rectangle(
            frame,
            (cx - size, cy - size),
            (cx + size, cy + size),
            (0, 255, 0),
            2
        )
        return frame

    def release(self):
        """釋放所有資源（等同 stop）。"""
        self.stop()


def main():
    """主程式：顯示即時影像，按 q 鍵離開。"""
    cam = RealSenseCamera(width=848, height=480, fps=60)
    cam.start()

    try:
        while True:
            frame = cam.get_frame()
            if frame is not None:
                cv2.imshow("RealSense Demo", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

