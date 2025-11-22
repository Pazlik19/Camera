import cv2

# Открываем камеру (0 - обычно CSI камера)
cap = cv2.VideoCapture(0)

# Проверяем, открылась ли камера
if not cap.isOpened():
    print("Ошибка: Не могу открыть камеру")
    exit()

print("Камера открыта успешно")

# Читаем один кадр
ret, frame = cap.read()

if ret:
    print(f"Кадр получен! Размер: {frame.shape}")
    
    # Сохраняем изображение
    cv2.imwrite('captured_image.jpg', frame)
    print("Изображение сохранено как 'captured_image.jpg'")
    
    # Показываем изображение
    cv2.imshow('Camera Feed', frame)
    cv2.waitKey(0)  # Ждем нажатия любой клавиши
else:
    print("Ошибка: Не удалось получить кадр")

# Освобождаем камеру
cap.release()
cv2.destroyAllWindows()