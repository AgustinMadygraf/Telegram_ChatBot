# bot/bot.py
import telegram
import os

async def send(reply_content, chat_id=593052206):
    """Envía un mensaje a un chat de Telegram específico."""
    token_telegram = os.getenv('telegram_token')
    bot = telegram.Bot(token_telegram)
    async with bot:
        await bot.send_message(chat_id=593052206, text=reply_content)

async def send_a():
    token_telegram = os.getenv('telegram_token')
    bot = telegram.Bot(token_telegram)
    async with bot:
        await bot.send_message(text='procesando', chat_id=593052206)
