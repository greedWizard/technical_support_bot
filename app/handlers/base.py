from telegram import Update
from telegram.ext import ContextTypes

from settings import get_settings


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=settings.GREETING_TEXT,
    )
