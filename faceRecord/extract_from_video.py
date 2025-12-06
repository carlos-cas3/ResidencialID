import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

FACE_SIZE = 200

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def augment_face_conservative(face_img):
    """
    Augmentación CONSERVADORA - Solo variaciones realistas que ayudan a LBPH.
    Genera 3-4 variaciones en lugar de 8.
    """
    augmented = []
    
    # 1. Original (SIEMPRE)
    augmented.append(face_img)
    
    # 2. Brillo ligero (+10%) - Simula diferente iluminación
    bright = cv2.convertScaleAbs(face_img, alpha=1.1, beta=8)
    augmented.append(bright)
    
    # 3. Brillo reducido (-10%) - Simula sombra ligera
    dark = cv2.convertScaleAbs(face_img, alpha=0.9, beta=-8)
    augmented.append(dark)
    
    # 4. Flip horizontal (espejo) - SOLO si ayuda (opcional)
    # Comentado por defecto porque puede confundir a LBPH
    # flipped = cv2.flip(face_img, 1)
    # augmented.append(flipped)
    
    return augmented


def extract_faces(video_path, nombre, skip_frames=2, max_faces=100, use_augmentation=True, residente_id=None):
    # Si quieres guardar por ID:
    if residente_id is not None:
        output_dir = f"dataset/{residente_id}_{nombre}"
    else:
        output_dir = f"dataset/{nombre}"
    
    ensure_dir(output_dir)


    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"[ERROR] No se pudo abrir el video: {video_path}")
        return

    frame_count = 0
    saved_faces = 0
    total_images = 0

    print(f"[INFO] Extrayendo rostros para '{nombre}'...")
    print(f"[INFO] Configuración: max_faces={max_faces}, augmentation={'Sí (conservadora)' if use_augmentation else 'No'}")

    while saved_faces < max_faces:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        
        # Procesar cada N frames
        if frame_count % skip_frames != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar rostros
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, w, h) in faces:
            if saved_faces >= max_faces:
                break
                
            # Extraer rostro con pequeño margen (5%)
            margin = int(w * 0.05)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(gray.shape[1], x + w + margin)
            y2 = min(gray.shape[0], y + h + margin)
            
            face_img = gray[y1:y2, x1:x2]

            # Redimensionar
            face_img = cv2.resize(face_img, (FACE_SIZE, FACE_SIZE))
            
            # Normalizar con ecualización de histograma
            face_img = cv2.equalizeHist(face_img)
            
            saved_faces += 1
            
            if use_augmentation:
                # Augmentación conservadora (3 variaciones)
                augmented_faces = augment_face_conservative(face_img)
                
                for idx, aug_face in enumerate(augmented_faces):
                    total_images += 1
                    filename = f"{output_dir}/face_{saved_faces:04d}_{idx}.jpg"
                    cv2.imwrite(filename, aug_face)
                    
                    # Mostrar solo la original
                    if idx == 0:
                        cv2.imshow("Capturando", aug_face)
            else:
                # Sin augmentación
                total_images += 1
                filename = f"{output_dir}/face_{saved_faces:04d}.jpg"
                cv2.imwrite(filename, face_img)
                cv2.imshow("Capturando", face_img)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n{'='*50}")
    print(f"[✓] Extracción completada para '{nombre}'")
    print(f"{'='*50}")
    print(f"  Rostros base:     {saved_faces}")
    print(f"  Imágenes totales: {total_images}")
    if use_augmentation and saved_faces > 0:
        print(f"  Ratio augment:    {total_images/saved_faces:.1f}x")
    print(f"{'='*50}\n")


def extract_faces_interactive(nombre, duration_seconds=20, target_faces=80):
    """
    Captura rostros en VIVO con instrucciones.
    MEJOR OPCIÓN para máxima variedad natural.
    """
    output_dir = f"dataset/{nombre}"
    ensure_dir(output_dir)
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("[ERROR] No se puede acceder a la cámara.")
        return
    
    print(f"\n{'='*60}")
    print(f"  CAPTURA INTERACTIVA - {nombre}")
    print(f"{'='*60}")
    print("  INSTRUCCIONES:")
    print("  1. Mantén el rostro centrado en el cuadro verde")
    print("  2. Gira la cabeza LENTAMENTE:")
    print("     - Izquierda → Centro → Derecha")
    print("     - Arriba → Centro → Abajo")
    print("  3. Cambia expresiones suavemente:")
    print("     - Sonríe → Serio → Sorprendido")
    print(f"  4. Duración: {duration_seconds} segundos")
    print(f"  5. Meta: {target_faces} capturas base")
    print("  6. Presiona ESC para terminar antes")
    print(f"{'='*60}\n")
    
    input("Presiona ENTER cuando estés listo...")
    
    start_time = cv2.getTickCount()
    freq = cv2.getTickFrequency()
    
    saved_faces = 0
    frame_count = 0
    last_save_time = 0
    min_interval = 0.2  # Guardar máximo cada 0.2 segundos
    
    while saved_faces < target_faces:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        current_time = (cv2.getTickCount() - start_time) / freq
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, 1.1, 5, minSize=(120, 120)
        )
        
        # Preparar frame para mostrar
        display_frame = frame.copy()
        
        # Dibujar guías y rostros
        h, w = display_frame.shape[:2]
        cv2.circle(display_frame, (w//2, h//2), 5, (0, 255, 255), -1)  # Centro
        
        for (x, y, fw, fh) in faces:
            cv2.rectangle(display_frame, (x, y), (x+fw, y+fh), (0, 255, 0), 2)
        
        # Tiempo restante
        remaining = max(0, duration_seconds - current_time)
        progress = (saved_faces / target_faces) * 100
        
        # Info en pantalla
        cv2.putText(display_frame, f"Tiempo: {remaining:.1f}s", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f"Capturas: {saved_faces}/{target_faces} ({progress:.0f}%)", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Instrucción actual
        if current_time < 7:
            instruction = "Mira al FRENTE"
        elif current_time < 13:
            instruction = "Gira la CABEZA lentamente"
        else:
            instruction = "Cambia EXPRESIONES"
        cv2.putText(display_frame, instruction, (10, h-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        cv2.imshow("Captura Interactiva", display_frame)
        
        # Guardar rostro si hay uno y ha pasado el intervalo mínimo
        if len(faces) == 1 and (current_time - last_save_time) >= min_interval:
            x, y, fw, fh = faces[0]
            
            # Margen pequeño
            margin = int(fw * 0.05)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(gray.shape[1], x + fw + margin)
            y2 = min(gray.shape[0], y + fh + margin)
            
            face_img = gray[y1:y2, x1:x2]
            face_img = cv2.resize(face_img, (FACE_SIZE, FACE_SIZE))
            face_img = cv2.equalizeHist(face_img)
            
            saved_faces += 1
            last_save_time = current_time
            
            # Augmentación conservadora
            augmented = augment_face_conservative(face_img)
            for idx, aug_face in enumerate(augmented):
                filename = f"{output_dir}/face_{saved_faces:04d}_{idx}.jpg"
                cv2.imwrite(filename, aug_face)
        
        # Verificar condiciones de salida
        if current_time >= duration_seconds or saved_faces >= target_faces:
            break
        
        if cv2.waitKey(1) & 0xFF == 27:
            print("\n[!] Captura cancelada por el usuario")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    total_images = saved_faces * 3  # 3 variaciones por rostro
    print(f"\n{'='*50}")
    print(f"[✓] Captura interactiva completada")
    print(f"{'='*50}")
    print(f"  Rostros base:     {saved_faces}")
    print(f"  Imágenes totales: {total_images}")
    print(f"  Calidad:          {'EXCELENTE' if saved_faces >= target_faces*0.8 else 'ACEPTABLE' if saved_faces >= target_faces*0.5 else 'BAJA - Repetir captura'}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    # Prueba interactiva
    extract_faces_interactive("test_user", duration_seconds=20, target_faces=80)