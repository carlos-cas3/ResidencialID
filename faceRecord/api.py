# microservicio/api.py - VERSIÓN CORREGIDA
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import os
import uuid
import cv2
import json
import time
from queue import Queue
import threading

from extract_from_video import extract_faces
from train_model import train_model

log_queue = Queue()

# ✅ Control global del stream
camera_active = False
camera_lock = threading.Lock()
current_cap = None

def log_event(message, level="info"):
    event = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message
    }
    log_queue.put(event)
    print(f"[LOG] {message}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

class DatasetRequest(BaseModel):
    resident_id: int
    nombre: str
    video_path: str
    max_faces: int = 100
    skip_frames: int = 2
    augmentation: bool = True

class TrainRequest(BaseModel):
    dataset_path: str = "./dataset"


@app.post("/generate-dataset")
def generate_dataset(request: DatasetRequest):
    try:
        log_event(f"Iniciando generación de dataset para {request.nombre} (ID: {request.resident_id})")
        
        temp_name = f"temp_{uuid.uuid4()}.mp4"
        temp_path = f"./temp_videos/{temp_name}"
        os.makedirs("./temp_videos", exist_ok=True)

        log_event("Descargando video desde Supabase...")
        response = requests.get(request.video_path, stream=True, timeout=30)
        
        if response.status_code != 200:
            log_event("Error: No se pudo descargar el video", "error")
            return {"status": "error", "message": "No se pudo descargar el video"}

        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        count = extract_faces(
            video_path=temp_path,
            residente_id=request.resident_id,
            nombre=request.nombre,
            skip_frames=request.skip_frames,
            max_faces=request.max_faces,
            use_augmentation=request.augmentation
        )

        os.remove(temp_path)
        log_event(f"Dataset generado: {count} imágenes", "success")
        
        return {
            "status": "success",
            "message": f"Dataset generado para {request.nombre}",
            "resident_id": request.resident_id,
            "images_count": count
        }

    except Exception as e:
        log_event(f"Error: {str(e)}", "error")
        return {"status": "error", "message": str(e)}


@app.post("/train-model")
def train(request: TrainRequest):
    try:
        log_event("Iniciando entrenamiento...")
        dataset_real = os.path.abspath(request.dataset_path)
        model_path = train_model(dataset_real)
        log_event("Modelo entrenado correctamente", "success")
        
        return {
            "status": "success",
            "message": "Modelo entrenado correctamente",
            "model_path": model_path
        }
    except Exception as e:
        log_event(f"Error: {str(e)}", "error")
        return {"status": "error", "message": str(e)}


from main import process_frame_with_logger

# ✅ Iniciar cámara manualmente
@app.post("/camera/start")
def start_camera():
    global camera_active, current_cap
    
    with camera_lock:
        if camera_active:
            return {"status": "already_running", "message": "La cámara ya está activa"}
        
        # ✅ Liberar cámara anterior si existe
        if current_cap is not None:
            current_cap.release()
            time.sleep(0.5)
        
        current_cap = cv2.VideoCapture(0)
        
        # ✅ Dar tiempo a la cámara para inicializar
        time.sleep(0.5)
        
        if not current_cap.isOpened():
            log_event("❌ No se pudo abrir la cámara", "error")
            current_cap = None
            return {"status": "error", "message": "No se pudo abrir la cámara"}
        
        # ✅ Verificar que pueda leer frames
        ret, _ = current_cap.read()
        if not ret:
            log_event("❌ La cámara se abrió pero no puede leer frames", "error")
            current_cap.release()
            current_cap = None
            return {"status": "error", "message": "La cámara no puede capturar frames"}
        
        camera_active = True
        log_event("✅ Cámara iniciada correctamente", "success")
        
        return {"status": "success", "message": "Cámara iniciada"}


# ✅ Detener cámara manualmente
@app.post("/camera/stop")
def stop_camera():
    global camera_active, current_cap
    
    with camera_lock:
        camera_active = False
        
        if current_cap is not None:
            current_cap.release()
            current_cap = None
        
        log_event("🔓 Cámara detenida", "warning")
        
        return {"status": "success", "message": "Cámara detenida"}


# ✅ Estado de la cámara
@app.get("/camera/status")
def camera_status():
    is_opened = current_cap.isOpened() if current_cap is not None else False
    return {
        "active": camera_active,
        "camera_opened": is_opened,
        "message": "Cámara activa" if camera_active else "Cámara inactiva"
    }


# ✅ Stream de video (solo funciona si la cámara está activa)
def gen_frames():
    global camera_active, current_cap
    
    log_event("📡 Cliente conectado al stream")
    
    # ✅ Verificar que la cámara esté abierta
    if current_cap is None or not current_cap.isOpened():
        log_event("❌ Stream solicitado pero cámara no disponible", "error")
        return
    
    frame_count = 0
    error_count = 0
    
    try:
        while camera_active:
            # ✅ Verificar que current_cap sigue existiendo
            if current_cap is None:
                log_event("⚠️ current_cap es None, terminando stream", "warning")
                break
            
            success, frame = current_cap.read()
            
            if not success:
                error_count += 1
                if error_count % 30 == 0:  # Log cada 30 errores
                    log_event(f"⚠️ No se pudo leer frame (errores: {error_count})", "warning")
                
                if error_count > 100:
                    log_event("❌ Demasiados errores leyendo frames, deteniendo stream", "error")
                    break
                
                time.sleep(0.01)
                continue
            
            # Reset error count si lee correctamente
            error_count = 0
            frame_count += 1
            
            # Log cada 60 frames (2 segundos aprox)
            if frame_count % 60 == 0:
                log_event(f"📊 Frame {frame_count} procesado correctamente", "info")
            
            processed = process_frame_with_logger(frame, log_event)
            ret, buffer = cv2.imencode('.jpg', processed)
            
            if not ret:
                continue
            
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )
    
    except GeneratorExit:
        log_event("🔌 Cliente desconectado del stream")
    
    except Exception as e:
        log_event(f"❌ Error en stream: {str(e)}", "error")
    
    finally:
        log_event(f"🏁 Stream finalizado. Total frames procesados: {frame_count}")


@app.get("/video-stream")
def video_stream():
    if not camera_active:
        log_event("⚠️ Intento de acceder al stream con cámara inactiva", "warning")
        return {"status": "error", "message": "La cámara no está activa. Usa POST /camera/start primero"}
    
    if current_cap is None or not current_cap.isOpened():
        log_event("❌ Cámara marcada como activa pero no está abierta", "error")
        return {"status": "error", "message": "Error: La cámara no está disponible"}
    
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


def stream_logs():
    while True:
        event = log_queue.get()
        yield f"data: {json.dumps(event)}\n\n"


@app.get("/events")
def events():
    return StreamingResponse(stream_logs(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)