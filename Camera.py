import cv2

def show_usb_camera():
    print("=== ЗАПУСК USB КАМЕРЫ ===")
    
    # Пробуем разные индексы камер
    for camera_index in [0, 1, 2]:
        print(f"Пробуем камеру с индексом {camera_index}...")
        cap = cv2.VideoCapture(camera_index)
        
        # Устанавливаем стандартные разрешения для теста
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if cap.isOpened():
            print(f"✓ Камера найдена на индексе {camera_index}")
            
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print("Ошибка чтения кадра")
                        break
                    
                    # Показываем информацию о кадре
                    height, width = frame.shape[:2]
                    cv2.putText(frame, f"Camera {camera_index} - {width}x{height}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    cv2.imshow('USB Camera', frame)
                    
                    # Выход по 'q' или ESC
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q') or key == 27:
                        break
                        
            finally:
                cap.release()
                cv2.destroyAllWindows()
            return
        else:
            print(f"✗ Камера не найдена на индексе {camera_index}")
    
    print("❌ Не удалось найти ни одну камеру")

if __name__ == "__main__":
    show_usb_camera()