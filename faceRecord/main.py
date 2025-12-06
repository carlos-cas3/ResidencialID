# microservicio/main.py
import cv2
import numpy as np
import time
import mediapipe as mp
import json
import os

from database import registrar_acceso, registrar_desconocido

# --- Inicializar mediapipe ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# --- Cargar el modelo 1 sola vez ---
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_model.xml')

# --- Cargar labels una vez ---
def load_labels(filename='labels.txt'):
    labels = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            label, name = line.strip().split(':')
            labels[int(label)] = name
    return labels

# --- Cargar mapping una vez ---
def load_mapping(filename='mapping.json'):
    if not os.path.exists(filename):
        print(f"[WARNING] {filename} no existe, usando labels directos")
        return {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar {filename}: {e}")
        return {}

labels = load_labels()
mapping = load_mapping()  # ← Cargar mapping.json

# --- Detector de caras Haar ---
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ============================================
#   PROCESA UN SOLO FRAME (INTEGRACIÓN STREAM)
# ============================================
last_marked = {}
unknown_frames = 0
last_unknown_time = 0

FACE_SIZE = 200
UNKNOWN_FRAMES_REQUIRED = 15
UNKNOWN_DELAY = 20  # segundos


def get_face_direction(frame, face_landmarks):
    h, w, _ = frame.shape

    left_cheek = face_landmarks.landmark[234]
    right_cheek = face_landmarks.landmark[454]

    left_x = int(left_cheek.x * w)
    right_x = int(right_cheek.x * w)

    return "Entrando" if left_x < right_x else "Saliendo"


def get_real_id(label_name):
    """
    Convierte el nombre del label al ID real de Supabase usando mapping.json
    
    Args:
        label_name: Nombre desde labels.txt (ej: "Carlos", "5", "DESCONOCIDO_Carlos")
    
    Returns:
        int o None: ID real de Supabase o None si no es válido
    """
    # ✅ Caso 1: El label ya es un número (sistema nuevo)
    try:
        return int(label_name)
    except (ValueError, TypeError):
        pass
    
    # ✅ Caso 2: Buscar en mapping.json (sistema antiguo)
    if label_name in mapping:
        try:
            return int(mapping[label_name])
        except (ValueError, TypeError):
            print(f"[WARNING] Mapping inválido para {label_name}: {mapping[label_name]}")
            return None
    
    # ✅ Caso 3: Label no válido
    print(f"[WARNING] No se encontró ID real para label: {label_name}")
    return None


def process_frame_with_logger(frame, log_event=None):
    """
    Procesa un frame con logging opcional
    """
    global unknown_frames, last_unknown_time

    if log_event is None:
        log_event = lambda msg, level="info": print(f"[{level.upper()}] {msg}")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)
    direction = "NoDetectado"

    if result.multi_face_landmarks:
        direction = get_face_direction(frame, result.multi_face_landmarks[0])

    current_time = time.time()

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face, (FACE_SIZE, FACE_SIZE))

        label, confidence = face_recognizer.predict(face_resized)

        # ===== RECONOCIDO =====
        if confidence < 60:
            unknown_frames = 0

            if label in labels:
                label_name = labels[label]
                
                # ✅ Convertir label a ID real usando mapping
                residente_id_real = get_real_id(label_name)
                
                # Nombre para mostrar en pantalla
                if residente_id_real is not None:
                    nombre = f"ID: {residente_id_real}"
                else:
                    nombre = str(label_name)
            else:
                residente_id_real = None
                nombre = "Desconocido?"

            # ✅ Registrar acceso solo si tenemos ID real válido
            if residente_id_real is not None:
                if current_time - last_marked.get(residente_id_real, 0) > 60:
                    registrar_acceso(residente_id_real, direction)
                    last_marked[residente_id_real] = current_time
                    log_event(f"Acceso registrado: Residente {residente_id_real} - {direction}", "success")
            else:
                # Persona reconocida pero sin ID válido
                if current_time - last_marked.get(label_name, 0) > 60:
                    log_event(f"Persona reconocida sin ID válido: {label_name} - {direction}", "warning")
                    last_marked[label_name] = current_time

            cv2.putText(frame, nombre, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # ===== DESCONOCIDO =====
        else:
            unknown_frames += 1

            if unknown_frames >= UNKNOWN_FRAMES_REQUIRED:
                if current_time - last_unknown_time > UNKNOWN_DELAY:
                    registrar_desconocido(direction)
                    last_unknown_time = current_time
                    log_event(f"Persona desconocida detectada - {direction}", "warning")

                cv2.putText(frame, "Desconocido", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Analizando...", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return frame


def process_frame(frame):
    """Versión original sin logging (por si se usa en otro lugar)"""
    return process_frame_with_logger(frame, log_event=None)