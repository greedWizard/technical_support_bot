CREATE_MAPPING_TABLE_SQL_QUERY = '''
CREATE TABLE IF NOT EXISTS chat_web_mapping (
    web_chat_id INTEGER,
    telegram_chat_id INTEGER,
    PRIMARY KEY (web_chat_id, telegram_chat_id)
);
'''
ADD_NEW_CHAT_INFO = '''
INSERT INTO chat_web_mapping (web_chat_id, telegram_chat_id) VALUES (
    ?, ?
);
'''
GET_CHAT_INFO_BY_TELEGRAM_ID = '''
SELECT web_chat_id, telegram_chat_id FROM chat_web_mapping
WHERE
telegram_chat_id = ?
LIMIT 1;
'''
GET_CHAT_INFO_BY_WEB_ID = '''
SELECT (web_chat_id, telegram_chat_id) FROM chat_web_mapping WHERE
web_chat_id = ?
LIMIT 1;
'''
GET_CHATS_COUNT = '''
SELECT COUNT(*) FROM chat_web_mapping WHERE
web_chat_id = ? OR telegram_chat_id = ?
'''
