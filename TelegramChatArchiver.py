import telegram
import os
import sys
import asyncio
import logging
from bot.archiver import cargar_datos_existentes
from shared_utils import datetime_to_unixtime, cargar_json, guardar_json
import config
from dotenv import load_dotenv
import time

load_dotenv()  # Carga las variables de entorno del archivo .env

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_REINTENTOS = 5  


def manejo_excepciones_telegram(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except telegram.error.NetworkError:
            logging.error("Error de red en Telegram.")
            # Implementar lógica específica, como reintentar la conexión
        except telegram.error.TimedOut:
            logging.error("Tiempo de espera agotado en Telegram.")
            # Implementar reintentos con backoff exponencial
        except telegram.error.TelegramError as e:
            logging.error(f"Error general de la API de Telegram: {e}")
        except Exception as e:
            logging.error(f"Error inesperado en {func.__name__}: {e}")
        return []
    return wrapper


def reintento_con_backoff_exponencial(func):
    async def wrapper(*args, **kwargs):
        reintento = 0
        tiempo_espera = 1  # Tiempo de espera inicial en segundos
        while reintento < MAX_REINTENTOS:
            try:
                return await func(*args, **kwargs)
            except (telegram.error.NetworkError, telegram.error.TimedOut):
                time.sleep(tiempo_espera)
                tiempo_espera *= 2  # Duplicar el tiempo de espera
                reintento += 1
        return None
    return wrapper


class TelegramArchiver:
    def __init__(self, token, chat_history_path):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_history_path = chat_history_path
        self.bot = telegram.Bot(self.token)


    @manejo_excepciones_telegram
    async def get_updates(self):
        async with self.bot:
            return await self.bot.get_updates(timeout=60)

    async def get_updates(self):
        try:
            async with self.bot:
                return await self.bot.get_updates(timeout=60)
        except telegram.error.TimedOut as e:
            logging.warning(f"Tiempo de espera agotado al intentar obtener actualizaciones: {e}")
            return []
        except telegram.error.NetworkError as e:
            logging.error(f"Error de red al intentar obtener actualizaciones: {e}")
            return []
        except telegram.error.TelegramError as e:
            logging.error(f"Error de la API de Telegram: {e}")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al obtener actualizaciones de Telegram: {e}")
            return []

    def process_updates(self, updates):
        data_existente = cargar_datos_existentes(self.chat_history_path)
        chat_histories = data_existente.get("chat_histories", {})
        user_info = data_existente.get("user_info", {})

        for update in updates:
            if update.message:
                self._process_message(update, chat_histories, user_info)

        for chat_id in chat_histories:
            chat_histories[chat_id].sort(key=lambda x: x['unixtime'], reverse=True)

        return chat_histories, user_info

    def _process_message(self, update, chat_histories, user_info):
        try:
            chat_id = str(update.message.chat.id)
            text = update.message.text
            update_id = update.update_id
            unixtime = datetime_to_unixtime(update.message.date)

            if chat_id not in chat_histories:
                chat_histories[chat_id] = []
            elif any(m["update_id"] == update_id for m in chat_histories[chat_id]):
                return  # Evitar duplicados

            chat_histories[chat_id].append({
                "role": "user",
                "content": text,
                "update_id": update_id,
                "unixtime": unixtime
            })

            user = update.message.from_user
            user_info[user.id] = {
                "username": user.username or 'Sin username',
                "first_name": user.first_name,
                "last_name": user.last_name or '',
                "id": user.id
            }
        except Exception as e:
            logging.error(f"Error al procesar el mensaje de Telegram: {e}")

    def save_chat_history(self, chat_histories, user_info):
        guardar_json(self.chat_history_path, {
            "chat_histories": chat_histories,
            "user_info": user_info
        })

async def main():
    if sys.version_info[0] >= 3:
        sys.stdout.reconfigure(encoding='utf-8')
    
    token_telegram = config.TELEGRAM_TOKEN
    archiver = TelegramArchiver(token_telegram, config.CHAT_HISTORY_PATH)

    updates = await archiver.get_updates()
    logging.info("Actualizaciones de Telegram recibidas")
    
    chat_histories, user_info = archiver.process_updates(updates)
    logging.info("Procesando actualizaciones de Telegram")

    archiver.save_chat_history(chat_histories, user_info)
    logging.info("Historial del chat guardado en archivo JSON")

if __name__ == '__main__':
    asyncio.run(main())
