from telegram import Update, Bot
from telegram.ext import ContextTypes

from containers.factories import get_container
from handlers.converters.chats import convert_chats_dtos_to_message
from services.chats import ChatsService
from services.web import BaseChatWebService


async def get_thread_name(bot: Bot, chat_id: int, message_thread_id: int) -> str:
    # Получаем первое сообщение в треде
    chat = await bot.get_chat(chat_id=chat_id)
    message = await chat.get_message(message_thread_id)
    # Возвращаем текст первого сообщения как название треда
    return message.text


async def get_all_chats_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)  # type: ignore
        chats = await service.get_all_chats()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text=convert_chats_dtos_to_message(chats=chats),
            parse_mode='MarkdownV2',
        )


async def set_chat_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)  # type: ignore
        await service.add_listener(
            telegram_chat_id=update.effective_chat.id,
            chat_oid=context.args[0],
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='Вы подключились к чату.',
            parse_mode='MarkdownV2',
        )


async def quit_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,  # type: ignore
        text='Вы вышли из диалога с клиентом.',
        parse_mode='MarkdownV2',
    )


async def send_message_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        web_service = await request_container.get(BaseChatWebService)  # type: ignore
        service = await request_container.get(ChatsService)
        chat_info = await service.get_chat_info_by_telegram_id(telegram_chat_id=update.message.message_thread_id)
        await web_service.send_message_to_chat(chat_oid=chat_info.web_chat_id, message_text=update.message.text)

