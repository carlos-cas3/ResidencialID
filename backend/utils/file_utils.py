import shutil
import uuid
from pathlib import Path

TEMP_DIR = Path("temp_videos")
TEMP_DIR.mkdir(exist_ok=True)

async def save_temp_video(file):
    """Guarda un video temporalmente."""
    file_id = str(uuid.uuid4())
    file_path = TEMP_DIR / f"{file_id}.mp4"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)
