import os
import json
from dotenv import load_dotenv
import logging
import sys

class ConfigManager:
    def __init__(self, config_file="config.json", setup_file="setup.json", default_model_path='E:\\Model _Explorer'):
        load_dotenv()
        self.config_data = self.load_json_file(config_file)
        self.system_template = self.load_system_template(setup_file)
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.model_path = os.getenv('MODEL_PATH', default_model_path)
        self.chat_history_path = self.config_data.get("chat_history_path", "data/context_window_telegram.json")

    @staticmethod
    def load_json_file(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Archivo '{file_path}' no encontrado. Usando configuración por defecto.")
        except json.JSONDecodeError:
            print(f"Error al decodificar '{file_path}'. Verifica el formato del archivo.")
        except Exception as e:
            print(f"Error al cargar '{file_path}': {e}")
        return {}

    def load_system_template(self, file_path):
        try:
            with open(file_path, "r") as file:
                templates = json.load(file)
                for idx, template in enumerate(templates, start=1):
                    print(f"{idx}. {template['modo']}")
                seleccion = input("Elige el modo (por número): ")
                seleccion_index = int(seleccion) - 1
                if 0 <= seleccion_index < len(templates):
                    return templates[seleccion_index]['system_template']
        except (FileNotFoundError, json.JSONDecodeError, ValueError, Exception) as e:
            print("Error al cargar '{file_path}' o selección inválida. Usando configuración por defecto.")
            return '### System:\nConfiguración por defecto.'
        return '### System:\nConfiguración por defecto.'

# Ejemplo de uso
config_manager = ConfigManager()

def cargar_configuracion(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logging.error(f"Archivo '{ruta_archivo}' no encontrado.")
        sys.exit("Error: Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        logging.error(f"Error al decodificar '{ruta_archivo}'. Verifica el formato del archivo.")
        sys.exit("Error: Formato de archivo de configuración inválido.")
    except Exception as e:
        logging.error(f"Error inesperado al cargar '{ruta_archivo}': {e}")
        sys.exit("Error inesperado al cargar la configuración.")


