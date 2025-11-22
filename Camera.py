import cv2

def imx219_live_stream(sensor_id=0):
    """Потоковое видео с камеры IMX219"""
    
    # Pipeline для плавного видео
    pipeline = (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        "video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! "
        "nvvidconv flip-method=0 ! "
        "video/x-raw, width=1280, height=720, format=BGRx ! "
        "videoconvert ! video/x-raw, format=BGR ! "
        "appsink drop=1"
    )
    
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("Ошибка открытия камеры")
        return
    
    print("Поток запущен. Нажмите 'q' для выхода, 's' для сохранения кадра")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Ошибка чтения кадра")
            break
        
        # Отображаем кадр
        cv2.imshow('IMX219 Live Stream', frame)
        
        # Обработка клавиш
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"imx219_frame_{frame_count:04d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Сохранен кадр: {filename}")
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    print("Поток остановлен")

# Запуск потока
imx219_live_stream()