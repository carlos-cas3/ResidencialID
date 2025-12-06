import requests
from config import MICROSERVICIO_URL

def process_video_residente(video_url: str, nombre: str):
    endpoint = f"{MICROSERVICIO_URL}/procesar_video"

    response = requests.post(endpoint, json={
        "video_url": video_url,
        "nombre": nombre
    })

    if response.status_code != 200:
        raise Exception("Error en microservicio")

    return response.json()
