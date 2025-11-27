import cv2
import requests
import time

# ESP32 Access Point IP adresi
ESP32_IP = "http://192.168.4.1"

# Yüz algılama için Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera açılamadı")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Yüzleri çerçeveleme
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Yüz sayısını ESP32'ye gönder
    try:
        requests.get(f"{ESP32_IP}/update", params={"count": len(faces)}, timeout=0.3)
    except requests.exceptions.RequestException:
        print("ESP32'ye bağlanılamadı, bağlantıyı kontrol et!")

    # Kamerada göster
    cv2.imshow("Yüz Algılama", frame)

    # 'q' tuşu ile çıkış
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
