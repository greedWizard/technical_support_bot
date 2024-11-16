from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers.errors import error_handler
from handlers.base import start_handler
from handlers.chats import get_all_chats_handlers, send_message_to_chat, set_chat_listener
from repositories.initialize import create_tables
from settings import get_settings


def get_app():
    settings = get_settings()
    application = ApplicationBuilder().token(token=settings.TG_BOT_TOKEN).build()

    start_command_handler = CommandHandler('start', start_handler)
    get_all_chats_command_handler = CommandHandler('chats', get_all_chats_handlers)
    set_chat_listener_handler = CommandHandler('listen_chat', set_chat_listener)
    message_handler = MessageHandler(
        filters=filters.TEXT & ~filters.COMMAND,
        callback=send_message_to_chat,
    )

    application.add_handler(start_command_handler)
    application.add_handler(get_all_chats_command_handler)
    application.add_handler(set_chat_listener_handler)
    application.add_handler(message_handler)
    application.add_error_handler(error_handler, block=True)

    create_tables()

    return application


if __name__ == '__main__':
    get_app().run_polling()
