import pandas as pd
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import datetime
import os

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def generar_reporte_excel():
    """Genera un archivo Excel con Residentes, Accesos y Tabla de Horas."""

    # 1. Obtener residentes
    residentes = supabase.table("residentes").select("*").execute().data
    df_residentes = pd.DataFrame(residentes)

    if "face_encoding" in df_residentes.columns:
        df_residentes["face_encoding"] = df_residentes["face_encoding"].astype(str)

    # 2. Obtener accesos + join
    accesos = supabase.table("accesos").select("""
        id,
        tipo,
        fecha,
        hora,
        imagen_url,
        residente_id,
        residentes ( nombre )
    """).execute().data

    for item in accesos:
        if item.get("residentes"):
            item["nombre_residente"] = item["residentes"]["nombre"]
        else:
            item["nombre_residente"] = "DESCONOCIDO"
        del item["residentes"]

    df_accesos = pd.DataFrame(accesos)

    # 2.1 convertir fecha
    if "fecha" in df_accesos.columns:
        df_accesos["fecha"] = pd.to_datetime(df_accesos["fecha"]).dt.date

    # ===============================================
    # 🔥 2.2 GENERAR COLUMNA HORA_INDICE (automático)
    # ===============================================

    if "hora" in df_accesos.columns:
        # convertir str → time
        df_accesos["hora"] = pd.to_datetime(df_accesos["hora"], format="%H:%M:%S").dt.time
        
        # extraer solo la hora
        df_accesos["hora_indice"] = df_accesos["hora"].apply(lambda t: t.hour)

    # 3. Crear tabla de horas
    horas = list(range(0, 24))
    df_horas = pd.DataFrame({
        "hora_decimal": horas,
        "hora_texto": [f"{h:02d}:00" for h in horas],
        "hora_excel": [datetime.time(h, 0, 0) for h in horas]
    })

    # 4. Guardar Excel
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Reporte_Condominio_{fecha_actual}.xlsx"

    os.makedirs("reportes", exist_ok=True)
    filepath = f"reportes/{filename}"

    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df_residentes.to_excel(writer, index=False, sheet_name="Residentes")
        df_accesos.to_excel(writer, index=False, sheet_name="Accesos")
        df_horas.to_excel(writer, index=False, sheet_name="Horas")

    print(f"[Reporte] Archivo generado en: {filepath}")

    return filepath
