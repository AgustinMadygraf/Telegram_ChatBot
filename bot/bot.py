import telegram
import os
import logging

async def send(reply_content, chat_id):
    """Envía un mensaje a un chat de Telegram específico."""
    token_telegram = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token_telegram)
    try:
        async with bot:
            await bot.send_message(chat_id, text=reply_content)
    except telegram.error.NetworkError as e:
        logging.error(f"Error de red al enviar mensaje: {e}")
    except telegram.error.TelegramError as e:
        logging.error(f"Error de la API de Telegram al enviar mensaje: {e}")
    except Exception as e:
        logging.error(f"Error inesperado al enviar mensaje: {e}")

async def send_a(chat_id):
    """Función de ejemplo para enviar un mensaje genérico."""
    token_telegram = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token_telegram)
    try:
        async with bot:
            await bot.send_message(chat_id, text='Procesando...')
    except telegram.error.NetworkError as e:
        logging.error(f"Error de red al enviar mensaje 'Procesando...': {e}")
    except telegram.error.TelegramError as e:
        logging.error(f"Error de la API de Telegram al enviar mensaje 'Procesando...': {e}")
    except Exception as e:
        logging.error(f"Error inesperado al enviar mensaje 'Procesando...': {e}")

