from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.errors import error_handler
from handlers.base import start_handler
from handlers.chats import get_all_chats_handlers, set_chat_listener
from settings import get_settings


def get_app():
    settings = get_settings()
    application = ApplicationBuilder().token(token=settings.TG_BOT_TOKEN).build()

    start_command_handler = CommandHandler('start', start_handler)
    get_all_chats_command_handler = CommandHandler('chats', get_all_chats_handlers)
    set_chat_listener_handler = CommandHandler('set_chat', set_chat_listener)

    application.add_handler(start_command_handler)
    application.add_handler(get_all_chats_command_handler)
    application.add_handler(set_chat_listener_handler)
    application.add_error_handler(error_handler, block=True)

    return application


if __name__ == '__main__':
    get_app().run_polling()
