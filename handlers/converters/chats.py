from dtos.mesages import ChatListItemDTO


def convert_chats_dtos_to_message(chats: list[ChatListItemDTO]) -> str:
    return '\n'.join(
        (
            'Список всех доступных чатов:',
            '\n'.join(
                (f'ChatOID: `{chat.oid}`\. Проблема: {chat.title}' for chat in chats)  # type: ignore
            )
        )
    )
