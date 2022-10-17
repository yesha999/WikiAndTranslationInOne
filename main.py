import sqlite3
import os
import wikipedia
from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery


bot = Client("my_bot", api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))
LANGUAGES = ["ru", "en", "zh-cn", "es", "ar", "pt", "ja", "de", "fr"]
WIKI_INFORMATION_LENGTH = 500


@bot.on_message(filters.command("start") & filters.private)
async def start_bot(bot: Client, message: Message):
    await message.reply_text(
        text=f"Привет **{message.from_user.first_name}** \n\n __Я самый умный и простой Бот-переводчик__")
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Русский", callback_data="ru"),
        InlineKeyboardButton("English", callback_data="en"),
        InlineKeyboardButton("中文", callback_data="zh-cn")],
        [InlineKeyboardButton("Español", callback_data="es"),
         InlineKeyboardButton("العربية", callback_data="ar"),
         InlineKeyboardButton("Português", callback_data="pt")],
        [InlineKeyboardButton("日本語", callback_data="ja"),
         InlineKeyboardButton("Deutsch", callback_data="de"),
         InlineKeyboardButton("Français", callback_data="fr")],
    ], )
    await message.reply_text("На какой язык переводить?", reply_markup=keyboard)


@bot.on_callback_query()
async def memorizing_language(bot: Client, answer_message: CallbackQuery):
    """
    Если пользователь впервые нажал /start, его запишем в базу данных и запомним язык, на который
    он хочет переводить, если же пользователь захочет изменить язык,
    он нажмет /start (или просто нажмет на keyboard button) и изменит его.
    """
    if answer_message.data in LANGUAGES:  # Можно было
        # бы обойтись без оператора IF, он сделан для случаев, если в дальнейшем развитии
        # приложения появятся другие callback_query
        try:
            with sqlite3.connect("tguser_lang.db") as connection:
                cursor = connection.cursor()
        except sqlite3.Error as error:
            await bot.send_message(answer_message.message.chat.id, "Ошибка соединения с БД")

        update_tguser_lang = (f"""
        INSERT INTO tguser_lang (tg_user_id, text_language) 
        VALUES ('{answer_message.from_user.id}', '{answer_message.data}')
        ON CONFLICT (tg_user_id) DO UPDATE SET text_language='{answer_message.data}'
        WHERE tg_user_id='{answer_message.from_user.id}';
        """)
        cursor.execute(update_tguser_lang)
        connection.commit()
        cursor.close()
        translator = Translator()
        translation = translator.translate("Язык выбран.", dest=answer_message.data, src='ru')
        await bot.send_message(answer_message.message.chat.id, translation.text)


def wiki_search(lang: str, text: str) -> str | None:
    wikipedia.set_lang(lang)
    try:
        wiki_title = wikipedia.search(text)[0]
    except:
        return None
    try:
        wiki_info = wikipedia.summary(wiki_title, sentences=3, chars=200)
    except wikipedia.exceptions.DisambiguationError as e:
        first_wiki_title = e.options[0]  # Если падает ошибка с неоднозначностью запроса,
        # выберем первый вариант
        wiki_info = wikipedia.summary(first_wiki_title, sentences=3, chars=200)
    return wiki_info


@bot.on_message(filters.text & filters.private)
async def translate(bot: Client, message: Message):
    try:
        with sqlite3.connect("tguser_lang.db") as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        await bot.send_message(message.chat.id, "Ошибка соединения с БД")

    select_query = f"""
    SELECT text_language from tguser_lang WHERE tg_user_id={message.from_user.id}
    """
    cursor.execute(select_query)
    records = cursor.fetchall()
    try:
        lang = records[0][0]
    except:
        lang = "en"  # Если пользователь не выбрал язык после /start, ему будет переводиться на английский,
        # в базу такого пользователя класть также необязательно
    cursor.close()

    translator = Translator()
    translation = translator.translate(message.text, dest=lang)
    await bot.send_message(message.chat.id, translation.text)

    source_language = translation.src if translation.src != 'ua' or 'mn' else source_language = "ru"
    # Иногда русский язык определяется как другой язык
    if source_language == "ru":  # Если начальный язык был русский, ищем в Вики на русском.
        wiki_text = wiki_search("ru", message.text[:300])
        if wiki_text is not None:
            await bot.send_message(message.chat.id, f"Вики: {wiki_text}")
    elif lang == "ru":  # Если перевод был на русский, ищем в Вики на русском
        wiki_text = wiki_search("ru", translation.text[:300])
        if wiki_text is not None:
            await bot.send_message(message.chat.id, f"Вики: {wiki_text}")
    else:
        # В иных случаях, ищем на языке написанного сообщения
        wiki_text = wiki_search(source_language, message.text[:300])
        if wiki_text is not None:
            await bot.send_message(message.chat.id, f"Wiki: {wiki_text}")


if __name__ == '__main__':
    bot.run()
