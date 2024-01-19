#main.py
import sys
import asyncio
from config_manager import ConfigManager, inicializar_entorno
from cycle_manager import ejecutar_ciclo_principal
from user_interaction_manager import obtener_opciones_usuario, seleccionar_modelo, inicializar_modelo_ia
from logs.config_logger import configurar_logging

config_manager = ConfigManager()  
logger = configurar_logging()

async def main():
    """
    Función principal para iniciar el chatbot de Telegram.

    Esta función se encarga de inicializar el entorno de ejecución, configurar la sesión de usuario y 
    gestionar el ciclo principal de ejecución del chatbot. Incluye la configuración de logging, la obtención de 
    opciones de usuario, la selección del modelo de IA y la ejecución del ciclo principal de mensajes.

    Parámetros:
    Ninguno

    Retorna:
    None
    """
    config = inicializar_entorno()
    logger.info("Inicio del programa")
    logger.info(f"Versión de Python: {sys.version}")
    logger.info("Inicializando...")
    logger.info(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")
    user_id_str = str(593052206)
    i = 2
    respuesta_rapida, ram_seleccionada = obtener_opciones_usuario(config)
    seleccion_modelo = seleccionar_modelo(config, ram_seleccionada)
    if seleccion_modelo:
        model = inicializar_modelo_ia(config, seleccion_modelo)
        if model:
            await ejecutar_ciclo_principal(model, config, user_id_str, seleccion_modelo, respuesta_rapida)
        else:
            logger.warning("No se pudo inicializar el modelo.")
    else:
        logger.warning("No se ha inicializado ningún modelo.")

if __name__ == '__main__':
    asyncio.run(main())
