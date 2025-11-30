"""
Módulo para captura de video y rostros desde la cámara.
"""
import cv2
import os
from tkinter import messagebox, filedialog


def capture_video(nombre, seconds=10):
    """Graba un video del residente durante N segundos."""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "No se pudo acceder a la cámara.")
        return None

    # Ruta donde guardamos el video
    video_path = f"../videos/{nombre}.mp4"
    os.makedirs("../videos", exist_ok=True)

    # Configuración del video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

    messagebox.showinfo(
        "Grabando...",
        f"Grabando video del residente '{nombre}' por {seconds} segundos.\n"
        "Por favor, mire al frente y mueva la cabeza suavemente."
    )

    start = cv2.getTickCount()
    freq = cv2.getTickFrequency()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        cv2.imshow("Grabando Video", frame)

        elapsed = (cv2.getTickCount() - start) / freq
        if elapsed >= seconds:
            break

        if cv2.waitKey(1) & 0xFF == 27:  # ESC para abortar
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return video_path


def capture_face():
    """Captura un rostro desde la cámara."""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("No se puede acceder a la cámara.")
        return None

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se puede capturar el frame.")
            break

        cv2.imshow("Captura de Rostro", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            if len(faces) == 1:
                x, y, w, h = faces[0]
                face = gray[y:y+h, x:x+w]
                cap.release()
                cv2.destroyAllWindows()
                return face
            else:
                messagebox.showerror("Error", "Debe haber exactamente 1 rostro.")

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


def upload_video(nombre):
    """Permite subir un video MP4/AVI desde archivos."""
    video_path = filedialog.askopenfilename(
        title="Seleccionar video del residente",
        filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")]
    )

    if not video_path:
        messagebox.showwarning("Cancelado", "No se seleccionó ningún video.")
        return None

    return video_path
