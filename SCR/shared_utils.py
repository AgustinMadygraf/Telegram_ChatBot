# shared_utils.py

import json
import os
import logging
import datetime

def cargar_json(archivo):
    """Carga un archivo JSON y devuelve su contenido."""
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo JSON {archivo}: {e}")
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {archivo}")
    return None

def guardar_json(archivo, datos):
    """Guarda datos en un archivo JSON."""
    try:
        with open(archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)
        logging.info(f"Datos guardados en {archivo}")
    except Exception as e:
        logging.error(f"No se pudo guardar en el archivo {archivo}. Error: {e}")

def datetime_to_unixtime(dt):
    """Convierte un objeto datetime a tiempo Unix."""
    return int(dt.timestamp())

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Agrega aquí cualquier otra función que creas que puede ser reutilizada en múltiples partes del proyecto.
