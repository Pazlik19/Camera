import cv2
import numpy as np

print("Проверка OpenCV...")
print(f"Версия OpenCV: {cv2.__version__}")

# Проверка доступных камер
for i in range(4):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✓ Камера на /dev/video{i} работает")
        else:
            print(f"✗ Камера на /dev/video{i} не возвращает кадры")
        cap.release()
    else:
        print(f"✗ Нет доступа к /dev/video{i}")