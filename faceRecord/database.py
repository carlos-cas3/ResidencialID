import datetime
import numpy as np
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# RESIDENTES
# ==========================================

def get_residentes():
    """Obtiene todos los residentes registrados."""
    result = supabase.table("residentes").select("*").execute()
    return result.data


def add_residente(nombre, face_encoding=None):
    """Crea un nuevo residente con su encoding facial y DEVUELVE EL ID REAL."""
    data = {"nombre": nombre}

    if isinstance(face_encoding, np.ndarray):
        data["face_encoding"] = face_encoding.tobytes()

    result = supabase.table("residentes").insert(data).execute()
    
    # CRÍTICO: Devolver el ID real generado por Supabase
    real_id = result.data[0]["id"]
    print(f"[Supabase] Residente agregado: {nombre} con ID={real_id}")
    return real_id  # ← ESTO ES LO IMPORTANTE


def add_residente_label(nombre):
    """Alias para agregar residente (mantiene compatibilidad)."""
    data = supabase.table("residentes").insert({"nombre": nombre}).execute()
    return data.data[0]["id"]


def get_residente_by_id(residente_id):
    """Obtiene un residente específico por ID."""
    result = supabase.table("residentes").select("*").eq("id", residente_id).execute()
    if result.data:
        return result.data[0]
    return None


# ==========================================
# ACCESOS (ENTRADAS / SALIDAS)
# ==========================================

def registrar_acceso(residente_id, tipo, imagen_url=None):
    """Registra entrada o salida de un residente."""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    data = {
        "residente_id": residente_id,
        "tipo": tipo,
        "fecha": fecha,
        "hora": hora,
        "imagen_url": imagen_url
    }

    supabase.table("accesos").insert(data).execute()
    print(f"[Supabase] ACCESO → {residente_id} | {tipo} | {fecha} {hora}")


# ==========================================
# DESCONOCIDOS
# ==========================================

def registrar_desconocido(tipo, imagen_url=None):
    """Registra intento de ingreso de persona NO reconocida."""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    data = {
        "residente_id": None,
        "tipo": tipo,
        "fecha": fecha,
        "hora": hora,
        "imagen_url": imagen_url
    }

    supabase.table("accesos").insert(data).execute()
    print(f"[Supabase] DESCONOCIDO → {tipo} | {fecha} {hora}")


# ==========================================
# CONSULTAR ACCESOS
# ==========================================

def obtener_accesos():
    """Devuelve el log completo con nombres."""
    query = supabase.table("accesos").select("""
        id,
        residente_id,
        tipo,
        fecha,
        hora,
        imagen_url,
        residentes ( nombre )
    """).execute()

    return query.data