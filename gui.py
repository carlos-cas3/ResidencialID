"""  
Interfaz gráfica principal para el sistema de control de acceso.
Este módulo maneja la creación de la ventana principal y la organización
de los componentes de la interfaz.
"""
import tkinter as tk
from functools import partial
from ui_styles import BUTTON_STYLE, LABEL_STYLE, ENTRY_STYLE, TITLE_STYLE, WINDOW_CONFIG
from callbacks import (
    add_residente_grabando_callback,
    add_residente_subiendo_callback,
    train_model_callback,
    run_recognition_callback,
    generar_reporte_callback
)



def create_main_window():
    """Crea y configura la ventana principal de la aplicación."""
    root = tk.Tk()
    root.title(WINDOW_CONFIG["title"])
    root.geometry(WINDOW_CONFIG["geometry"])
    root.configure(bg=WINDOW_CONFIG["bg"])
    return root


def create_title(root):
    """Crea el título principal de la aplicación."""
    title_label = tk.Label(
        root,
        text="Control de Acceso - Condominio",
        **TITLE_STYLE
    )
    title_label.pack(pady=20)


def create_name_input(root):
    """Crea el campo de entrada para el nombre del residente."""
    instruction_label = tk.Label(
        root,
        text="Nombre del residente:",
        **LABEL_STYLE
    )
    instruction_label.pack()

    name_entry = tk.Entry(root, **ENTRY_STYLE)
    name_entry.pack(pady=10)
    return name_entry


def create_buttons(root, name_entry):
    """Crea todos los botones de la interfaz."""
    # Botones para agregar residente
    tk.Button(
        root,
        text="Grabar Video del Residente",
        **BUTTON_STYLE,
        command=partial(add_residente_grabando_callback, name_entry)
    ).pack(pady=10)

    tk.Button(
        root,
        text="Subir Video del Residente",
        **BUTTON_STYLE,
        command=partial(add_residente_subiendo_callback, name_entry)
    ).pack(pady=10)

    # Botones para entrenar y reconocer
    tk.Button(
        root,
        text="Entrenar Modelo",
        **BUTTON_STYLE,
        command=train_model_callback
    ).pack(pady=10)

    tk.Button(
        root,
        text="Iniciar Reconocimiento",
        **BUTTON_STYLE,
        command=run_recognition_callback
    ).pack(pady=10)

    # Botón para generar reporte
    tk.Button(
        root,
        text="Generar Reporte Excel",
        **BUTTON_STYLE,
        command=generar_reporte_callback
    ).pack(pady=10)


def main():
    """Función principal que inicializa la aplicación."""
    root = create_main_window()
    create_title(root)
    name_entry = create_name_input(root)
    create_buttons(root, name_entry)
    root.mainloop()


if __name__ == "__main__":
    main()
