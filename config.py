import os
import json
from dotenv import load_dotenv

load_dotenv()

def load_system_template():
    try:
        with open("setup.json", "r") as file:
            templates = json.load(file)
            for idx, template in enumerate(templates, start=1):
                print(f"{idx}. {template['modo']}")
            seleccion = input("Elige el modo (por número): ")
            try:
                seleccion_index = int(seleccion) - 1
                if 0 <= seleccion_index < len(templates):
                    return templates[seleccion_index]['system_template']
            except ValueError:
                pass
            print("Selección inválida. Usando configuración por defecto.")
            return templates[0]['system_template']
    except FileNotFoundError:
        print("Archivo 'setup.json' no encontrado. Usando configuración por defecto.")
        return '### System:\nConfiguración por defecto.'
    except json.JSONDecodeError:
        print("Error al decodificar 'setup.json'. Verifica el formato del archivo.")
        return '### System:\nConfiguración por defecto.'
    except Exception as e:
        print(f"Error inesperado al cargar 'setup.json': {e}")
        return '### System:\nConfiguración por defecto.'

SYSTEM_TEMPLATE = load_system_template()

CHAT_HISTORY_PATH = "data/context_window_telegram.json"

MODELOS_POR_RAM = {
    "1": "1 GB",
    "2": "4 GB",
    "3": "8 GB",
    "4": "16 GB"
}

MODELOS_DISPONIBLES = {
    # tus modelos disponibles aquí
}

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
MODEL_PATH = os.getenv('MODEL_PATH', 'E:\Model _Explorer')
