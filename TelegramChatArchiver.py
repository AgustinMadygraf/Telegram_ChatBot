#TelegramChatArchiver.py
from bot.archiver import cargar_datos_existentes
from bot.utils import datetime_to_unixtime

import asyncio
import telegram
import os
import json
import sys



if sys.version_info[0] >= 3:
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    if sys.version_info[0] >= 3:
        sys.stdout.reconfigure(encoding='utf-8')
    token_telegram = os.getenv('telegram_token')
    bot = telegram.Bot(token_telegram)
    async with bot:
        historial = await bot.get_updates()

        archivo = "context_window_telegram.json"
        data_existente = cargar_datos_existentes(archivo)

        chat_histories = data_existente.get("chat_histories", {})
        user_info = data_existente.get("user_info", {})

        for update in historial:
            if update.message:
                chat_id = str(update.message.chat.id)  # Asegurarse de que chat_id sea una cadena
                text = update.message.text
                update_id = update.update_id
                message_date = update.message.date

                unixtime = datetime_to_unixtime(message_date)

                if chat_id not in chat_histories:
                    chat_histories[chat_id] = []
                elif any(mensaje["update_id"] == update_id for mensaje in chat_histories[chat_id]):
                    continue  # Evitar agregar mensajes duplicados

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

        for chat_id, messages in chat_histories.items():
            chat_histories[chat_id] = sorted(messages, key=lambda x: x['unixtime'], reverse=True)


        data_to_save = {
            "chat_histories": chat_histories,
            "user_info": user_info
        }

        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    asyncio.run(main())
