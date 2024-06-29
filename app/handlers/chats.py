import re
from telegram import Update
from telegram.ext import ContextTypes

from containers.factories import get_container
from handlers.constants import SEND_MESSAGE_STATE
from handlers.converters.chats import convert_chats_dtos_to_message
from services.web import BaseChatWebService


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


async def start_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,  # type: ignore
        text=(
            'Теперь вы отвечаете на сообщения. Выберите сообщение и '
            'напишите ответ. Пользователь увидит ваш ответ на сайте.'
        ),
    )

    return SEND_MESSAGE_STATE


async def quit_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,  # type: ignore
        text='Вы вышли из диалога с клиентом.',
        parse_mode='MarkdownV2',
    )


async def send_message_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message is None:  # type: ignore
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='Ошибка! Выберите сообщение на которое вы отвечаете.',
        )
        return

    print(update.message.reply_to_message.text)
    try:
        # TODO: сделать паттерн под UUID4
        chat_oid = re.findall(r'\s{1}\(.+\)', update.message.reply_to_message.text)[0].replace(
            ' ', '',
        ).replace('(', '').replace(')', '')
    except IndexError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='Необходимо ответить именно на сообщение пользователя.',
        )
        return

    print(chat_oid,)
