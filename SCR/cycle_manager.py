#cycle_manager.py
import TelegramChatArchiver
from bot.processing import cargar_chat_history, procesar_respuesta
from bot.bot import send_a
import logging
import time
import asyncio
from logs.config_logger import configurar_logging

logger = configurar_logging()

async def ejecutar_ciclo_principal(model, config, user_id_str, seleccion_modelo, respuesta_rapida):
    """
    Ejecuta el ciclo principal de procesamiento de mensajes para el chatbot.
    """
    await iniciar_sesion_chat(model, config)
    await ciclo_de_procesamiento(model, config, user_id_str, seleccion_modelo, respuesta_rapida)

async def iniciar_sesion_chat(model, config):
    """
    Inicia sesión de chat con el modelo de IA utilizando la plantilla de sistema.
    """
    with model.chat_session(config['system_templates'][1]['template']):
        pass  # Aquí puedes incluir cualquier lógica inicial específica de la sesión si es necesario

async def ciclo_de_procesamiento(model, config, user_id_str, seleccion_modelo, respuesta_rapida):
    """
    Ciclo continuo que procesa los mensajes entrantes y responde.
    """
    seg = 5
    while True:
        await obtener_y_procesar_mensajes(model, config, user_id_str, seleccion_modelo, respuesta_rapida, seg)
        seg = await manejo_espera(seg)

async def obtener_y_procesar_mensajes(model, config, user_id_str, seleccion_modelo, respuesta_rapida, seg):
    """
    Obtiene y procesa mensajes de Telegram.
    """
    await TelegramChatArchiver.main()
    chat_history, user_info, ultimo_rol = cargar_chat_history(config['chat_history_path'])
    logging.info(f"Último mensaje en la conversación: rol '{ultimo_rol}'")
    if ultimo_rol == "user":
        await send_a(593052206)
        await procesar_respuesta(chat_history, user_id_str, model, 2, user_info, seleccion_modelo, config['telegram_token'], respuesta_rapida)

async def manejo_espera(seg):
    """
    Maneja la espera entre la recepción de mensajes.
    """
    logging.info("Esperando consulta desde Telegram")
    for seg_temp in range(seg, 0, -1):
        print(f"Continuando en {seg_temp} segundos...", end="\r")
        await asyncio.sleep(1)
    return min(seg + 1, 6)  # Aumenta el tiempo de espera hasta un máximo de 6 segundos
