import os
import json
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()
        self.config_data = self.load_json_file("config.json")
        self.system_template = self.load_json_file("setup.json")
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.model_path = os.getenv('MODEL_PATH', 'E:\\Model _Explorer')

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

# Uso del ConfigManager en otros archivos
config_manager = ConfigManager()
