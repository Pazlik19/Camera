import cv2
import subprocess

def get_camera_via_gstreamer(sensor_id=0):
    """Использование GStreamer для работы с камерой через tegra_camera_ctrl"""
    
    # GStreamer pipeline для NVIDIA камер
    pipeline = (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        "video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! "
        "nvvidconv ! video/x-raw, format=BGRx ! "
        "videoconvert ! video/x-raw, format=BGR ! "
        "appsink drop=1"
    )
    
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    return cap

# Использование
cap = get_camera_via_gstreamer(0)

if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('tegra_camera_image.jpg', frame)
        print("Изображение сохранено!")
    cap.release()
else:
    print("Не удалось открыть камеру")