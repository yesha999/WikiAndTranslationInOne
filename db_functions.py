import sqlite3

from pyrogram import Client
from pyrogram.types import CallbackQuery, Message


def change_user_language(bot: Client, answer_message: CallbackQuery):
    try:
        with sqlite3.connect("tguser_lang.db") as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    update_tguser_lang = (f"""
    INSERT INTO tguser_lang (tg_user_id, text_language) 
    VALUES ('{answer_message.from_user.id}', '{answer_message.data}')
    ON CONFLICT (tg_user_id) DO UPDATE SET text_language='{answer_message.data}'
    WHERE tg_user_id='{answer_message.from_user.id}';
    """)
    cursor.execute(update_tguser_lang)
    connection.commit()
    cursor.close()


def check_user_language(message: Message) -> str:
    try:
        with sqlite3.connect("tguser_lang.db") as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        return "en"

    select_query = f"""
    SELECT text_language from tguser_lang WHERE tg_user_id={message.from_user.id}
    """
    cursor.execute(select_query)
    records = cursor.fetchall()
    try:
        lang = records[0][0]
    except:
        lang = "en"  # Если пользователь не выбрал язык после /start, ему будет переводиться на английский
    cursor.close()
    return lang


def check_user_wiki_enabled(message: Message) -> int:
    try:
        with sqlite3.connect("tguser_lang.db") as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        return 1

    select_query = f"""
    SELECT wiki_enabled from tguser_lang WHERE tg_user_id={message.from_user.id}
    """
    cursor.execute(select_query)
    records = cursor.fetchall()
    try:
        wiki_enabled = records[0][0]
    except:
        wiki_enabled = 1  # Если пользователь не найден, пусть получает сообщения из вики
    cursor.close()
    return wiki_enabled


def off_wiki_enabled(message: Message):
    try:
        with sqlite3.connect("tguser_lang.db") as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    update_tguser_lang = (f"""
    INSERT INTO tguser_lang (tg_user_id, wiki_enabled) 
    VALUES ('{message.from_user.id}', 0)
    ON CONFLICT (tg_user_id) DO UPDATE SET wiki_enabled=0
    WHERE tg_user_id='{message.from_user.id}';
    """)
    cursor.execute(update_tguser_lang)
    connection.commit()
    cursor.close()


def on_wiki_enabled(message: Message):
    try:
        with sqlite3.connect("tguser_lang.db") as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    update_tguser_lang = (f"""
    INSERT INTO tguser_lang (tg_user_id, wiki_enabled) 
    VALUES ('{message.from_user.id}', 1)
    ON CONFLICT (tg_user_id) DO UPDATE SET wiki_enabled=1
    WHERE tg_user_id='{message.from_user.id}';
    """)
    cursor.execute(update_tguser_lang)
    connection.commit()
    cursor.close()
