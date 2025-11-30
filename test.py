import cv2

def detectar_camaras(max_devices=10):
    """
    Intenta abrir cámaras desde 0 hasta max_devices-1.
    Devuelve una lista con los índices de cámaras que funcionan.
    """
    disponibles = []
    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"[OK] Cámara encontrada en el índice {i}")
            disponibles.append(i)
            cap.release()
        else:
            print(f"[INFO] No hay cámara en el índice {i}")
    return disponibles

def probar_url(url):
    """
    Intenta abrir una cámara vía URL (por ejemplo, DroidCam o IP Webcam)
    """
    cap = cv2.VideoCapture(url)
    if cap.isOpened():
        print(f"[OK] Cámara encontrada en la URL: {url}")
        cap.release()
        return True
    else:
        print(f"[INFO] No se pudo abrir la cámara en la URL: {url}")
        return False

if __name__ == "__main__":
    print("Buscando cámaras locales...")
    camaras = detectar_camaras(max_devices=5)

    # Ejemplo: probar cámara Android vía URL
    url_android = " http://"
    print("\nProbando cámara Android vía URL...")
    probar_url(url_android)
