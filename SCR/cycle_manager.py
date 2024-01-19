#cycle_manager.py
import TelegramChatArchiver
from bot.processing import cargar_chat_history, procesar_respuesta
from bot.bot import send_a
import logging
import time

async def ejecutar_ciclo_principal(model, config, user_id_str, seleccion_modelo, respuesta_rapida):
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