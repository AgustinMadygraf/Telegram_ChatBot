import telegram
import json
import os
import sys
from bot.archiver import cargar_datos_existentes
from bot.utils import datetime_to_unixtime
import config
import asyncio

class TelegramArchiver:
    def __init__(self, token, chat_history_path):
        self.bot = telegram.Bot(token)
        self.chat_history_path = chat_history_path

    async def get_updates(self):
        try:
            async with self.bot:
                return await self.bot.get_updates(timeout=60)  # Aumentar el tiempo de espera a 60 segundos
        except telegram.error.TimedOut:
            print("Tiempo de espera agotado al intentar obtener actualizaciones. Reintentando...")
            return []
        except Exception as e:
            print(f"Ocurrió un error al obtener actualizaciones: {e}")
            return []

    def process_updates(self, updates):
        data_existente = cargar_datos_existentes(self.chat_history_path)
        chat_histories = data_existente.get("chat_histories", {})
        user_info = data_existente.get("user_info", {})

        for update in updates:
            if update.message:
                self._process_message(update, chat_histories, user_info)

        # Ordenar mensajes por unixtime de manera descendente (más recientes primero)
        for chat_id in chat_histories:
            chat_histories[chat_id].sort(key=lambda x: x['unixtime'], reverse=True)

        return chat_histories, user_info

    def _process_message(self, update, chat_histories, user_info):
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

    def save_chat_history(self, chat_histories, user_info):
        data_to_save = {
            "chat_histories": chat_histories,
            "user_info": user_info
        }

        with open(self.chat_history_path, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

async def main():
    if sys.version_info[0] >= 3:
        sys.stdout.reconfigure(encoding='utf-8')

    token_telegram = os.getenv('telegram_token')
    archiver = TelegramArchiver(token_telegram, config.CHAT_HISTORY_PATH)
    
    updates = await archiver.get_updates()
    chat_histories, user_info = archiver.process_updates(updates)
    archiver.save_chat_history(chat_histories, user_info)

if __name__ == '__main__':
    asyncio.run(main())