# ResidencialID

Sistema de reconocimiento facial para la gestión de accesos en una
edificio residencial.\
Este proyecto utiliza Python, OpenCV, MediaPipe y Supabase.

------------------------------------------------------------------------

## 1. Copiar repositorio

``` bash
git clone https://github.com/carlos-cas3/ResidencialID.git
```
------------------------------------------------------------------------

## 2. Crear entorno virtual
``` bash
python -m venv venv
```
------------------------------------------------------------------------

## 3. Activar entorno virtual
**Windows:**
``` bash
venv\Scripts\activate
```
------------------------------------------------------------------------

## 4. Instalar dependencias
``` bash
pip install -r requirements.txt
```
------------------------------------------------------------------------

## 5. Configuración de Supabase

Crear el archivo:
    config.py
Dentro colocar:
``` python
SUPABASE_URL = "TU_URL_AQUI"
SUPABASE_KEY = "TU_SUPABASE_KEY_AQUI"
```
------------------------------------------------------------------------
## 6 Ejecutar el sistema

``` bash
python gui.py
```
------------------------------------------------------------------------
