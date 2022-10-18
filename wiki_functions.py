import random

import wikipedia
from googletrans.models import Translated
from pyrogram import Client
from pyrogram.types import Message

WIKI_INFORMATION_LENGTH = 200
WIKI_SENTENCES = 2

def wiki_search(lang: str, text: str) -> str | None:
    wikipedia.set_lang(lang)
    try:
        wiki_title = wikipedia.search(text)[0]
    except:
        return None
    try:
        wiki_info = wikipedia.summary(wiki_title, sentences=WIKI_SENTENCES, chars=WIKI_INFORMATION_LENGTH)
    except wikipedia.exceptions.DisambiguationError as e:
        first_wiki_title = random.choice(e.options)  # Если падает ошибка с неоднозначностью запроса,
        # выберем рандомный вариант
        wiki_info = wikipedia.summary(first_wiki_title, sentences=WIKI_SENTENCES, chars=WIKI_INFORMATION_LENGTH)
    if len(wiki_info) < 150: # Если мало текста, можно еще пару предложений добавить.
        wiki_info = wikipedia.summary(wiki_title, sentences=WIKI_SENTENCES + 2, chars=WIKI_INFORMATION_LENGTH)
    return wiki_info


async def wiki_message(bot: Client, message: Message, translation: Translated, lang: str, source_language: str):
    if source_language == "ru":  # Если начальный язык был русский, ищем в Вики на русском.
        wiki_text = wiki_search("ru", message.text[:150])
        if wiki_text is not None:
            await bot.send_message(message.chat.id, f"Вики: {wiki_text}")
    elif lang == "ru":  # Если перевод был на русский, ищем в Вики на русском
        wiki_text = wiki_search("ru", translation.text[:150])
        if wiki_text is not None:
            await bot.send_message(message.chat.id, f"Вики: {wiki_text}")
    else:
        # В иных случаях, ищем на языке написанного сообщения
        wiki_text = wiki_search(source_language, message.text[:150])
        if wiki_text is not None:
            await bot.send_message(message.chat.id, f"Wiki: {wiki_text}")
