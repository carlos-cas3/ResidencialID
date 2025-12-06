from config import SUPABASE_URL, SUPABASE_KEY, MICROSERVICIO_URL
from supabase import create_client
import requests

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
#     FUNCIONES BD
# -------------------------

def insert_residente(nombre: str, dni: str, departamento: str, video_url: str):
    data = {
        "nombre": nombre,
        "dni": dni,
        "departamento": departamento,
        "video_url": video_url,
        "estado": "activo",
        "necesita_entrenamiento": True,
    }

    response = supabase.table("residentes").insert(data).execute()
    return response.data[0]


def get_all_residentes():
    return supabase.table("residentes").select("*").execute().data


def get_residente_by_id(residente_id: int):
    res = supabase.table("residentes").select("*").eq("id", residente_id).execute()
    return res.data[0] if res.data else None


def update_residente_db(residente_id: int, payload: dict):
    return (
        supabase.table("residentes")
        .update(payload)
        .eq("id", residente_id)
        .execute()
        .data
    )


def delete_residente_db(residente_id: int):
    return (
        supabase.table("residentes")
        .update({"estado": "inactivo"})
        .eq("id", residente_id)
        .execute()
        .data
    )



def get_training_candidates_db():
    return (
        supabase.table("residentes")
        .select("*")
        .eq("necesita_entrenamiento", True)
        .neq("video_url", "")
        .eq("estado", "activo")
        .execute()
        .data
    )



def get_all_accesos():
    response = supabase.table("accesos").select("""
        id,
        tipo,
        fecha,
        hora,
        imagen_url,
        residente_id,
        residentes ( nombre )
    """).execute()

    data = response.data or []

    for item in data:
        if item.get("residentes"):
            item["nombre_residente"] = item["residentes"]["nombre"]
        else:
            item["nombre_residente"] = "DESCONOCIDO"
        item.pop("residentes", None)

    return data


# -------------------------
#   LLAMADA AL MICROSERVICIO
# -------------------------

def call_microservice_generate_dataset(resident):
    body = {
        "resident_id": resident["id"],
        "nombre": resident["nombre"],
        "video_path": resident["video_url"],
        "max_faces": 100,
        "skip_frames": 2,
        "augmentation": True,
    }
    res = requests.post(f"{MICROSERVICIO_URL}/generate-dataset", json=body, timeout=300)
    
    return res.json()