import os
import json
from dotenv import load_dotenv
import sys
from bot.utils import limpiar_pantalla
from logs.config_logger import configurar_logging

logger = configurar_logging()

def inicializar_entorno():
    """
    Inicializa el entorno para la ejecución del chatbot de Telegram.

    Esta función configura el sistema de logging y carga la configuración inicial del bot. 
    La configuración se carga principalmente desde un archivo JSON. La función también 
    puede incluir pasos adicionales necesarios para preparar el entorno de ejecución, 
    como la limpieza de la pantalla de la consola.

    Retorna:
    dict: Un diccionario que contiene la configuración cargada del bot.
    """
    #limpiar_pantalla()
    return cargar_configuracion_inicial()


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


config_manager = ConfigManager()

def cargar_configuracion(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logger.error(f"Archivo '{ruta_archivo}' no encontrado.")
        sys.exit("Error: Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar '{ruta_archivo}'. Verifica el formato del archivo.")
        sys.exit("Error: Formato de archivo de configuración inválido.")
    except Exception as e:
        logger.error(f"Error inesperado al cargar '{ruta_archivo}': {e}")
        sys.exit("Error inesperado al cargar la configuración.")

def inicializar_entorno():
    #limpiar_pantalla()
    return cargar_configuracion_inicial()

def cargar_configuracion_inicial():
    """
    Inicializa y carga la configuración inicial del programa.
    Retorna un objeto de configuración.
    """
    # Configuración del logging
    logger.info("Inicio del programa")


    # Cargar configuración desde un archivo JSON
    try:
        config = cargar_configuracion('config.json')
        logger.info("Configuración cargada correctamente.")
    except FileNotFoundError:
        logger.error("Archivo 'config.json' no encontrado.")
        sys.exit("Error: Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        logger.error("Error al decodificar 'config.json'. Verifica el formato del archivo.")
        sys.exit("Error: Formato de archivo de configuración inválido.")
    except Exception as e:
        logger.error(f"Error inesperado al cargar 'config.json': {e}")
        sys.exit("Error inesperado al cargar la configuración.")

    return config