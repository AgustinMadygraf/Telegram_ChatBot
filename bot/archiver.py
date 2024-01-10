import json
import os
import logging

def cargar_datos_existentes(archivo):
    """Carga datos existentes desde un archivo JSON."""
    try:
        if os.path.exists(archivo) and os.path.getsize(archivo) > 0:
            with open(archivo, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            logging.info(f"El archivo {archivo} está vacío o no existe. Creando estructura predeterminada.")
            return {"chat_histories": {}, "user_info": {}}
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo JSON {archivo}: {e}")
        logging.info("Creando estructura de datos predeterminada debido a un error de decodificación.")
        return {"chat_histories": {}, "user_info": {}}
    except Exception as e:
        logging.error(f"Error inesperado al leer el archivo {archivo}: {e}")
        return {"chat_histories": {}, "user_info": {}}
