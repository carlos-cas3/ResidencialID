import cv2
import numpy as np
import time
import mediapipe as mp

# ⬅ Importar funciones de Supabase
from database import registrar_acceso, registrar_desconocido

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)


def load_labels(filename='labels.txt'):
    labels = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            label, name = line.strip().split(':')
            labels[int(label)] = name
    return labels


def get_face_direction(frame, face_landmarks):
    h, w, _ = frame.shape

    left_cheek = face_landmarks.landmark[234]
    right_cheek = face_landmarks.landmark[454]

    left_x = int(left_cheek.x * w)
    right_x = int(right_cheek.x * w)

    return "Entrando" if left_x < right_x else "Saliendo"


def run_recognition():

    print("[INFO] Cargando modelo facial...")
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('face_model.xml')

    labels = load_labels()

    print("[INFO] Iniciando cámara...")
    video_capture = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    last_marked = {}
    unknown_frames = 0
    UNKNOWN_FRAMES_REQUIRED = 15
    last_unknown_time = 0
    UNKNOWN_DELAY = 20
    unknown_counter = 0
    FACE_SIZE = 200

    while True:

        ret, frame = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)
        direction = "NoDetectado"

        if result.multi_face_landmarks:
            direction = get_face_direction(frame, result.multi_face_landmarks[0])

        current_time = time.time()

        for (x, y, w, h) in faces:

            # ---- Redimensionar antes del reconocimiento ----
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (FACE_SIZE, FACE_SIZE))

            label, confidence = face_recognizer.predict(face_resized)

            # ----- Reconocido -----
            if confidence < 60:
                if label in labels:
                    residente_id_real = labels[label]   # ← ID real de Supabase
                    residente_nombre = str(residente_id_real)
                else:
                    residente_id_real = None
                    residente_nombre = "Desconocido"

                unknown_frames = 0

                # Registrar solo si existe el ID real
                if residente_id_real is not None:
                    if current_time - last_marked.get(residente_id_real, 0) > 60:

                        registrar_acceso(residente_id_real, direction)
                        last_marked[residente_id_real] = current_time

                        print(f"[OK] Residente {residente_id_real} - {direction}")
                else:
                    print("⚠ Label detectado pero no está en labels.txt")

                cv2.putText(
                    frame, residente_nombre, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2
                )


            else:
                # ----- Desconocido -----
                unknown_frames += 1

                if unknown_frames >= UNKNOWN_FRAMES_REQUIRED:
                    if current_time - last_unknown_time > UNKNOWN_DELAY:
                        registrar_desconocido(direction)
                        last_unknown_time = current_time
                        print(f"[WARN] Desconocido → {direction}")

                    cv2.putText(
                        frame, "Desconocido", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2
                    )
                else:
                    cv2.putText(
                        frame, "Analizando...", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
                    )

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Reconocimiento Facial + Dirección", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ---- ESTO DEBE IR FUERA DEL WHILE ----
    video_capture.release()
    cv2.destroyAllWindows()
