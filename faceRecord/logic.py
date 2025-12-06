from video_capture import capture_video
from extract_from_video import extract_faces
from database import add_residente
from mapping_manager import registrar_residente_en_mapping, MAPPING_FILE

def registrar_residente_backend(nombre: str):
    """
    Lógica sin GUI para registrar un residente grabando un video.
    Retorna un diccionario con el resultado.
    """

    nombre = nombre.strip()
    if not nombre:
        return {"status": "error", "message": "Debe ingresar el nombre del residente."}

    try:
        # 1. Grabar video
        video_path = capture_video(nombre)
        if not video_path:
            return {"status": "error", "message": "El video no se pudo grabar."}

        # 2. Extraer caras
        extract_faces(video_path, nombre)

        # 3. Registrar en Supabase y obtener ID
        real_id = add_residente(nombre)
        if not real_id:
            return {"status": "error", "message": "No se pudo obtener el ID en Supabase."}

        # 4. Actualizar mapping.json
        registrar_residente_en_mapping(nombre, real_id)

        return {
            "status": "ok",
            "nombre": nombre,
            "real_id": real_id,
            "dataset": f"dataset/{nombre}/",
            "mapping": MAPPING_FILE
        }

    except Exception as e:
        return {"status": "error", "message": f"Error interno: {e}"}
