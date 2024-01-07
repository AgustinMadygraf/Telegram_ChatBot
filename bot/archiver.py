# bot/archiver.py

import json
import os

def cargar_datos_existentes(archivo):
    """Carga datos existentes desde un archivo JSON."""
    try:
        if os.path.exists(archivo) and os.path.getsize(archivo) > 0:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as file:
                return json.load(file)
        else:
            return {"chat_histories": {}, "user_info": {}}
    except json.JSONDecodeError as e:
        print(f"Error al leer el archivo JSON: {e}")
        return {"chat_histories": {}, "user_info": {}}