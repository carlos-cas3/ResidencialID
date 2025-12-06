from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import requests

from services.supabase_service import upload_video_to_supabase
from services.db_services import (
    insert_residente,
    get_all_residentes,
    get_residente_by_id,
    update_residente_db,
    delete_residente_db,
    get_training_candidates_db,
    call_microservice_generate_dataset
)

router = APIRouter(prefix="/residentes")


# -----------------------------
#   MODELO PARA ENTRENAMIENTO
# -----------------------------
class TrainDatasetRequest(BaseModel):
    resident_id: int
    nombre: str
    video_path: str
    max_faces: int = 100
    skip_frames: int = 2
    augmentation: bool = True

# -----------------------------
#   ENDPOINTS CRUD
# -----------------------------

@router.post("/upload")
async def upload_residente_video(
    video: UploadFile = File(...),
    nombre: str = Form(...),
    dni: str = Form(...),
    departamento: str = Form(...)
):
    video_bytes = await video.read()
    video_url = upload_video_to_supabase(video_bytes, video.filename)
    residente = insert_residente(nombre, dni, departamento, video_url)

    return {"status": "ok", "residente": residente}


@router.get("/")
async def get_residentes():
    return {"status": "ok", "data": get_all_residentes()}

# -----------------------------
#   ENTRENAMIENTO
# -----------------------------

@router.get("/training-candidates")
def get_training_candidates():
    return {"status": "ok", "data": get_training_candidates_db()}


class TrainDatasetIds(BaseModel):
    residentes: list[int]

@router.post("/train-dataset")
def train_dataset(data: TrainDatasetIds):
    results = []
    for resident_id in data.residentes:
        resident = get_residente_by_id(resident_id)
        if not resident:
            continue
        result = call_microservice_generate_dataset(resident)
        update_residente_db(resident_id, {"necesita_entrenamiento": False})
        results.append(result)
    return {"status": "ok", "result": results}


@router.get("/{residente_id}")
async def get_residente(residente_id: int):
    data = get_residente_by_id(residente_id)
    if not data:
        return {"status": "error", "msg": "Residente no encontrado"}
    return {"status": "ok", "data": data}


@router.put("/{residente_id}")
def update_residente(residente_id: int, payload: dict):
    updated = update_residente_db(residente_id, payload)
    return {"status": "ok", "updated": updated}


@router.delete("/{residente_id}")
def delete_residente(residente_id: int):
    deleted = delete_residente_db(residente_id)
    return {"status": "ok", "deleted": deleted}


