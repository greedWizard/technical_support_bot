from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from handlers.constants import SEND_MESSAGE_STATE
from handlers.errors import error_handler
from handlers.base import start_handler
from handlers.chats import get_all_chats_handlers, quit_chat, send_message_to_chat, set_chat_listener, start_dialog
from settings import get_settings


def get_app():
    settings = get_settings()
    application = ApplicationBuilder().token(token=settings.TG_BOT_TOKEN).build()

    start_command_handler = CommandHandler('start', start_handler)
    get_all_chats_command_handler = CommandHandler('chats', get_all_chats_handlers)
    set_chat_listener_handler = CommandHandler('listen_chat', set_chat_listener)
    start_dialog_handler = CommandHandler('start_dialog', start_dialog)
    quit_chat_handler = CommandHandler('quit', quit_chat)
    send_chat_messages_handler = ConversationHandler(
        entry_points=[start_dialog_handler],
        states={
            SEND_MESSAGE_STATE: [
                MessageHandler(
                    filters=filters.TEXT & ~ filters.COMMAND,
                    callback=send_message_to_chat,
                ),
            ]
        },
        fallbacks=(quit_chat_handler, )
    )

    application.add_handler(start_command_handler)
    application.add_handler(get_all_chats_command_handler)
    application.add_handler(set_chat_listener_handler)
    application.add_handler(send_chat_messages_handler)
    application.add_error_handler(error_handler, block=True)

    return application


if __name__ == '__main__':
    get_app().run_polling()
