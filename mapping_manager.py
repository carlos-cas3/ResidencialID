"""
Módulo para gestionar el archivo mapping.json que asocia
nombres de carpetas con IDs reales de Supabase.
"""
import json
import os
from tkinter import messagebox

MAPPING_FILE = "mapping.json"


def load_mapping():
    """Carga el mapping carpeta -> ID real de Supabase."""
    if not os.path.exists(MAPPING_FILE):
        print(f"[INFO] {MAPPING_FILE} no existe, creando uno nuevo...")
        return {}
    
    try:
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:  # Archivo vacío
                print(f"[WARNING] {MAPPING_FILE} está vacío, inicializando...")
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"[ERROR] {MAPPING_FILE} está corrupto: {e}")
        print("[INFO] Creando backup y reiniciando mapping...")
        # Hacer backup del archivo corrupto
        if os.path.exists(MAPPING_FILE):
            backup_name = f"{MAPPING_FILE}.backup"
            os.rename(MAPPING_FILE, backup_name)
            print(f"[INFO] Backup guardado como {backup_name}")
        return {}
    except Exception as e:
        print(f"[ERROR] Error inesperado al cargar mapping: {e}")
        return {}


def save_mapping(mapping):
    """Guarda el mapping actualizado."""
    try:
        with open(MAPPING_FILE, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        print(f"✅ Mapping guardado correctamente en {MAPPING_FILE}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el mapping: {e}")
        messagebox.showerror("Error", f"No se pudo guardar {MAPPING_FILE}: {e}")


def registrar_residente_en_mapping(nombre, real_id):
    """Asocia la carpeta del residente con su ID real de Supabase."""
    try:
        mapping = load_mapping()
        mapping[nombre] = real_id
        save_mapping(mapping)
        print(f"✅ Mapping actualizado: {nombre} -> ID {real_id}")
    except Exception as e:
        print(f"[ERROR] Error al registrar en mapping: {e}")
        messagebox.showerror("Error", f"No se pudo actualizar mapping: {e}")
