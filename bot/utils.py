# bot/utils.py

import os
import datetime
import time
import json

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def datetime_to_unixtime(dt):
    """Convierte un objeto datetime a tiempo Unix."""
    return int(dt.timestamp())


def guardar_chat_history(chat_history, user_info, chat_history_path, chat_id, reply_content, seleccion_modelo):
    try:
        # Agregar reply_content al historial de chat para el chat_id específico
        if chat_id not in chat_history:
            chat_history[chat_id] = []

        chat_history[chat_id].append({
            "role": seleccion_modelo,
            "content": reply_content,
            "update_id": len(chat_history[chat_id]),  # Usar la longitud de la lista como update_id
            "unixtime": int(time.time())
        })

        data = {
            "chat_histories": chat_history,
            "user_info": user_info
        }

        with open(chat_history_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"No se pudo guardar el historial del chat. Error: {e}")

