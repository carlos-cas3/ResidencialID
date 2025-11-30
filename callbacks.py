"""
Callbacks para los botones de la interfaz gráfica.
"""
from tkinter import messagebox
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from train_model import train_model
from main import run_recognition
from database import add_residente
from extract_from_video import extract_faces
from reportes_excel import generar_reporte_excel
from mapping_manager import registrar_residente_en_mapping, MAPPING_FILE
from video_capture import capture_video, upload_video


def add_residente_grabando_callback(name_entry):
    """Callback para agregar residente grabando video."""
    nombre = name_entry.get().strip()
    if not nombre:
        messagebox.showerror("Error", "Debe ingresar el nombre del residente.")
        return

    try:
        # 1. ✅ Grabar video
        video_path = capture_video(nombre)
        if not video_path:
            messagebox.showerror("Error", "El video no se pudo grabar.")
            return

        # 2. ✅ Extraer caras al dataset
        extract_faces(video_path, nombre)

        # 3. ✅ Registrar en Supabase y obtener ID REAL
        real_id = add_residente(nombre)
        
        if not real_id:
            messagebox.showerror("Error", "No se pudo obtener el ID de Supabase.")
            return
        
        # 4. ✅ Actualizar mapping.json
        registrar_residente_en_mapping(nombre, real_id)

        messagebox.showinfo(
            "Éxito",
            f"✅ Residente '{nombre}' registrado con ID={real_id}\n"
            f"Dataset generado en dataset/{nombre}/\n"
            f"Mapping actualizado en {MAPPING_FILE}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar residente: {e}")
        print(f"[ERROR] {e}")


def add_residente_subiendo_callback(name_entry):
    """Callback para agregar residente subiendo video."""
    nombre = name_entry.get().strip()
    if not nombre:
        messagebox.showerror("Error", "Debe ingresar el nombre del residente.")
        return

    try:
        # 1. ✅ Subir video
        video_path = upload_video(nombre)
        if not video_path:
            return

        # 2. ✅ Extraer caras al dataset
        extract_faces(video_path, nombre)

        # 3. ✅ Registrar en Supabase y obtener ID REAL
        real_id = add_residente(nombre)
        
        if not real_id:
            messagebox.showerror("Error", "No se pudo obtener el ID de Supabase.")
            return
        
        # 4. ✅ Actualizar mapping.json
        registrar_residente_en_mapping(nombre, real_id)

        messagebox.showinfo(
            "Éxito",
            f"✅ Residente '{nombre}' registrado con ID={real_id}\n"
            f"Dataset generado en dataset/{nombre}/\n"
            f"Mapping actualizado en {MAPPING_FILE}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar residente: {e}")
        print(f"[ERROR] {e}")


def train_model_callback():
    """Callback para entrenar el modelo."""
    try:
        train_model()
        messagebox.showinfo("Éxito", "Modelo entrenado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo entrenar: {e}")


def run_recognition_callback():
    """Callback para iniciar el reconocimiento facial."""
    try:
        run_recognition()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el reconocimiento: {e}")


def generar_reporte_callback():
    """Callback para generar reporte Excel."""
    try:
        path = generar_reporte_excel()
        messagebox.showinfo("Reporte generado", f"El archivo se creó en:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")
