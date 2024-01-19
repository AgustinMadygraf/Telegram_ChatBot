#main.py
import json
import time
import sys
import asyncio
from gpt4all import GPT4All
import TelegramChatArchiver
from bot.utils import limpiar_pantalla
from bot.bot import send_a
from bot.processing import cargar_chat_history, procesar_respuesta
from utils.logger import setup_logging
import logging
from config_manager import ConfigManager
from config_manager import cargar_configuracion

config_manager = ConfigManager()  # Instancia del nuevo gestor de configuraciones

setup_logging()

async def main():
    config = inicializar_logger_y_configuracion()
    logging.info("Inicio del programa")
    limpiar_pantalla()
    logging.info(f"Versión de Python: {sys.version}")
    logging.info("Inicializando...")
    logging.info(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")
    user_id_str = str(593052206)
    i = 2
    respuesta_rapida, ram_seleccionada = obtener_opciones_usuario(config)
    seleccion_modelo = seleccionar_modelo(config, ram_seleccionada)
    if seleccion_modelo:
        model = inicializar_modelo_ia(config, seleccion_modelo)
        if model:
            i = 2
            seg = 5
            with model.chat_session(config['system_templates'][0]['template']):
                while True:
                    await TelegramChatArchiver.main()
                    chat_history, user_info, ultimo_rol = cargar_chat_history(config['chat_history_path'])
                    logging.info(f"Último mensaje en la conversación: rol '{ultimo_rol}'")
                    if ultimo_rol == "user":     
                        seg = 5
                        await send_a(593052206)  
                        await procesar_respuesta(chat_history, user_id_str, model, i, user_info, seleccion_modelo, config['telegram_token'], respuesta_rapida)
                    else:
                        logging.info("Esperando consulta desde Telegram")
                        for seg_temp in range(seg, 0, -1):
                            print(f"Continuando en {seg_temp} segundos...", end="\r")
                            time.sleep(1)
                        if seg < 6:
                            seg += 1

                        await TelegramChatArchiver.main()
        else:
            logging.warning("No se pudo inicializar el modelo.")
    else:
        logging.warning("No se ha inicializado ningún modelo.")

def inicializar_logger_y_configuracion():
    # Configuración del logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Cargar configuración
    try:
        config = cargar_configuracion('config.json')
        logging.info("Configuración cargada correctamente.")
        return config
    except FileNotFoundError:
        logging.error("Archivo 'config.json' no encontrado.")
        sys.exit("Error: Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        logging.error("Error al decodificar 'config.json'. Verifica el formato del archivo.")
        sys.exit("Error: Formato de archivo de configuración inválido.")
    except Exception as e:
        logging.error(f"Error inesperado al cargar 'config.json': {e}")
        sys.exit("Error inesperado al cargar la configuración.")

def obtener_opciones_usuario(config):
    print("Elige el modo de respuesta del bot:")
    print("1. Respuesta rápida (ventana de contexto limitada a la última pregunta)")
    print("2. Respuesta detallada (ventana de contexto ampliada a todo el historial)")
    modo_respuesta = input("Selecciona una opción (1 o 2): ")
    if modo_respuesta not in ["1", "2"]:
        print("Selección inválida. Usando modo de respuesta rápida por defecto.")
        modo_respuesta = "1"

    respuesta_rapida = modo_respuesta == "1"

    opcion_ram = input("Selecciona la capacidad de tu memoria RAM: 1 (1 GB), 2 (4 GB), 3 (8 GB), 4 (16 GB): \n")
    if opcion_ram not in config['ram_options']:
        opcion_ram = "2"
    ram_seleccionada = config['ram_options'].get(opcion_ram)

    return respuesta_rapida, ram_seleccionada

def inicializar_modelo_ia(config, seleccion_modelo):
    try:
        inicio_carga = time.time()  # Iniciar el contador de tiempo
        print("Inicializando modelo de IA...")
        model = GPT4All(seleccion_modelo, config['model_path'])
        fin_carga = time.time()  # Finalizar el contador de tiempo
        tiempo_carga = fin_carga - inicio_carga  # Calcular la duración de la carga
        logging.info(f"Modelo inicializado con éxito en {tiempo_carga:.2f} segundos.")
        return model
    except ValueError as e:
        logging.error(f"Error al inicializar el modelo: {e}")
        return None

def seleccionar_modelo(config, ram_seleccionada):
    modelos_a_mostrar = config['models_available'].get(ram_seleccionada, [])
    if modelos_a_mostrar:
        logging.info(f"Modelos disponibles para RAM de {ram_seleccionada} seleccionada:")
        for idx, modelo in enumerate(modelos_a_mostrar, 1):
            logging.info(f"{idx}. {modelo}")
        seleccion_numero = input("\nSelecciona el número del modelo: ")
        if seleccion_numero.isdigit() and 1 <= int(seleccion_numero) <= len(modelos_a_mostrar):
            return modelos_a_mostrar[int(seleccion_numero) - 1]
    return None

if __name__ == '__main__':
    asyncio.run(main())
