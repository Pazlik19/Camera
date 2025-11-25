import cv2
import subprocess
import sys

def check_camera_availability():
    """Проверяет доступность камеры и компонентов"""
    print("=== Проверка системы ===")
    
    # Проверяем наличие видео устройств
    try:
        result = subprocess.run(['ls', '/dev/video*'], capture_output=True, text=True)
        print("Видео устройства:", result.stdout)
    except Exception as e:
        print("Ошибка при проверке видео устройств:", e)
    
    # Проверяем GStreamer
    try:
        result = subprocess.run(['gst-inspect-1.0', '--version'], capture_output=True, text=True)
        print("GStreamer версия:", result.stdout)
    except Exception as e:
        print("GStreamer не установлен:", e)

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=1 max-buffers=1"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
    print("=== Запуск камеры ===")
    check_camera_availability()
    
    window_title = "CSI Camera"
    
    # Пробуем разные sensor-id
    for sensor_id in [0, 1]:
        print(f"Пробуем sensor-id={sensor_id}")
        pipeline = gstreamer_pipeline(sensor_id=sensor_id, flip_method=0)
        print("GStreamer pipeline:", pipeline)
        
        video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        
        if video_capture.isOpened():
            print(f"✓ Камера найдена с sensor-id={sensor_id}")
            try:
                while True:
                    ret_val, frame = video_capture.read()
                    if not ret_val:
                        print("Ошибка чтения кадра")
                        break
                    
                    cv2.imshow(window_title, frame)
                    
                    keyCode = cv2.waitKey(10) & 0xFF
                    if keyCode == 27 or keyCode == ord('q'):
                        break
            finally:
                video_capture.release()
                cv2.destroyAllWindows()
            return
        else:
            print(f"✗ Камера не найдена с sensor-id={sensor_id}")
    
    print("=== Альтернативные методы ===")
    # Пробуем стандартный OpenCV
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Найдена камера через OpenCV с индексом {i}")
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Camera {i}", frame)
                cv2.waitKey(3000)
                cv2.destroyAllWindows()
            cap.release()

if __name__ == "__main__":
    show_camera()