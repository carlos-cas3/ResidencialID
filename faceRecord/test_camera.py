# test_camera_direct.py
import cv2
import time

print("Intentando abrir cámara...")
cap = cv2.VideoCapture(0)

print(f"¿Cámara abierta? {cap.isOpened()}")

if cap.isOpened():
    print("Intentando leer frames...")
    for i in range(10):
        ret, frame = cap.read()
        print(f"Frame {i}: {'✅ OK' if ret else '❌ FALLO'}")
        if ret:
            print(f"  Tamaño: {frame.shape}")
        time.sleep(0.1)
    
    cap.release()
    print("✅ Test completado")
else:
    print("❌ No se pudo abrir la cámara")