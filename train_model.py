import cv2
import os
import numpy as np
import json

FACE_SIZE = 200
BASE_DIR = "dataset"
MAPPING_FILE = "mapping.json"  
LABELS_OUT = "labels.txt"
MODEL_OUT = "face_model.xml"

def augment_image(image):
    augmented_images = []
    rows, cols = image.shape[:2]

    # Rotación leve
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 8, 1)
    rotated = cv2.warpAffine(image, M, (cols, rows))
    augmented_images.append(rotated)

    # Brillo leve
    bright = cv2.convertScaleAbs(image, alpha=1.1, beta=15)
    augmented_images.append(bright)

    # Pequeño recorte y resize (más conservador)
    if rows > 40 and cols > 40:
        cropped = image[6:rows-6, 6:cols-6]
        cropped = cv2.resize(cropped, (cols, rows))
        augmented_images.append(cropped)

    # (Opcional) flip horizontal — úsalo con precaución
    flipped = cv2.flip(image, 1)
    augmented_images.append(flipped)

    return augmented_images

def normalize_image(image):
    # equalize para mejorar contraste
    return cv2.equalizeHist(image)

def load_mapping():
    """Carga el mapping carpeta -> ID real de Supabase."""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_mapping(mapping):
    """Guarda el mapping actualizado."""
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

def load_images(base_dir):
    faces = []
    labels = []
    folder_list = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])

    for model_label, folder_name in enumerate(folder_list):
        label_path = os.path.join(base_dir, folder_name)
        for image_name in os.listdir(label_path):
            image_path = os.path.join(label_path, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue
            # resize y normalize
            image = cv2.resize(image, (FACE_SIZE, FACE_SIZE))
            image = normalize_image(image)
            faces.append(image)
            labels.append(model_label)

            # augment
            for aug in augment_image(image):
                aug = cv2.resize(aug, (FACE_SIZE, FACE_SIZE))
                aug = normalize_image(aug)
                faces.append(aug)
                labels.append(model_label)

    return faces, labels, folder_list

def train_model():
    mapping = load_mapping()  # Cargar mapping existente

    faces, labels, folder_list = load_images(BASE_DIR)
    if len(faces) == 0:
        raise RuntimeError("No hay imágenes en dataset/. Asegúrate de extraer caras antes de entrenar.")

    # convertir a numpy
    faces_np = np.array(faces)
    labels_np = np.array(labels)

    # LBPH espera lista de imágenes (no necesariamente un array 4D)
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, labels_np)
    face_recognizer.write(MODEL_OUT)

    # ✅ Crear labels.txt con IDs REALES de Supabase
    with open(LABELS_OUT, "w", encoding="utf-8") as f:
        for model_label, folder_name in enumerate(folder_list):
            if folder_name in mapping:
                # ✅ Usar el ID real de Supabase
                id_real = mapping[folder_name]
                f.write(f"{model_label}:{id_real}\n")
            else:
                # ⚠️ ADVERTENCIA: Esta carpeta no tiene ID en Supabase
                print(f"⚠️ ADVERTENCIA: '{folder_name}' no tiene ID en mapping.json")
                f.write(f"{model_label}:DESCONOCIDO_{folder_name}\n")

    print("✅ Modelo entrenado y guardado correctamente.")
    print(f"   Modelo: {MODEL_OUT}")
    print(f"   Labels: {LABELS_OUT}")
    print(f"   Mapping: {MAPPING_FILE}")

if __name__ == "__main__":
    train_model()