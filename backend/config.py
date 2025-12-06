import os
from dotenv import load_dotenv

load_dotenv()  # Carga el archivo .env automáticamente

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("SUPABASE_BUCKET", "residentes_videos")
SUPABASE_KEY_SERVICE_ROLE = os.getenv("SUPABASE_KEY_SERVICE_ROLE")
MICROSERVICIO_URL = os.getenv("MICROSERVICIO_URL")
