from config import SUPABASE_URL, SUPABASE_KEY_SERVICE_ROLE, BUCKET_NAME
from supabase import create_client
import uuid

# Crear cliente Supabase usando variables del .env
supabase = create_client(SUPABASE_URL, SUPABASE_KEY_SERVICE_ROLE)

def upload_video_to_supabase(file_bytes, filename: str):
    unique_name = f"{uuid.uuid4()}_{filename}"

    res = supabase.storage.from_(BUCKET_NAME).upload(
        unique_name,
        file_bytes,
        file_options={"content-type": "video/mp4"}  # opcional
    )

    if res is None:
        raise Exception("Error al subir archivo a Supabase")

    # Obtener URL PUBLICA
    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_name)

    return public_url
