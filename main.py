import os

from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from db_functions import change_dest_user_language, check_user_wiki_enabled, off_wiki_enabled, \
    on_wiki_enabled, change_src_user_language, check_user_dest_language, check_user_src_language
from keyboards import dest_languages_keyboard, src_languages_keyboard, lang_keyboard
from wiki_functions import wiki_message

bot = Client("my_bot", api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))

LANGUAGES = ["ru", "en", "zh-cn", "es", "ar", "pt", "ja", "de", "fr", "tr"]
SRC_LANGUAGES = ["src_ru", "src_en", "src_zh-cn", "src_es", "src_ar", "src_pt", "src_ja", "src_de", "src_fr", "tr",
                 "src_auto"]
EXCEPTION_LANGUAGES = ["uk", "mn", "be", "ky", "kk", "tg", "mk", "bg"]


@bot.on_message(filters.command("lang") & filters.private)
async def change_dest_language(bot: Client, message: Message):
    await message.reply_text("На какой язык переводить?", reply_markup=dest_languages_keyboard)


@bot.on_message(filters.command("start") & filters.private)
async def start_bot(bot: Client, message: Message):
    await message.reply_text(
        text=f"Привет **{message.from_user.first_name}** \n\n __Я самый умный и простой Бот-переводчик__")
    await change_dest_language(bot, message)


@bot.on_message(filters.command("offwiki") & filters.private)
async def off_wiki(bot: Client, message: Message):
    off_wiki_enabled(message)
    await bot.send_message(message.from_user.id, "Mode: No Wikipedia")


@bot.on_message(filters.command("onwiki") & filters.private)
async def on_wiki(bot: Client, message: Message):
    on_wiki_enabled(message)
    await bot.send_message(message.from_user.id, "Mode: Wikipedia")


@bot.on_callback_query()
async def choose_lang_menu(bot: Client, answer_message: CallbackQuery):
    """
    Если пользователь впервые нажал /start, его запишем в базу данных и запомним язык, на который
    он хочет переводить.
    """
    if answer_message.data in LANGUAGES:
        change_dest_user_language(bot, answer_message)  # Меняем целевой язык в базе данных
        translator = Translator()
        translation = translator.translate("Язык перевода выбран.", dest=answer_message.data, src='ru')
        await answer_message.edit_message_text(translation.text, reply_markup=lang_keyboard)
    if answer_message.data == "page_2":
        await answer_message.edit_message_text("С какого языка переводить?",
                                               reply_markup=src_languages_keyboard)
    if answer_message.data == "page_1":
        await answer_message.edit_message_text("На какой язык переводить?", reply_markup=dest_languages_keyboard)

    if answer_message.data in SRC_LANGUAGES:
        change_src_user_language(bot, answer_message)  # Меняем язык ввода в базе данных
        src_lang = answer_message.data[4:]  # Стираем src_
        if src_lang == "auto":
            await answer_message.edit_message_text("Язык ввода определяется автоматически", reply_markup=lang_keyboard)
        else:
            translator = Translator()
            translation = translator.translate("Язык ввода выбран.", dest=src_lang, src='ru')
            await answer_message.edit_message_text(translation.text, reply_markup=lang_keyboard)


@bot.on_message(filters.text & filters.private)
async def translate_and_wiki(bot: Client, message: Message):
    dest_lang = check_user_dest_language(message)
    src_lang = check_user_src_language(message)
    translator = Translator()
    translation = translator.translate(message.text, dest=dest_lang, src=src_lang)
    source_language = translation.src
    if source_language in EXCEPTION_LANGUAGES:  # Иногда русский язык определяется как другой язык,
        # Пример: слово "баг" определяется как монгольское и перевод неправильный.
        source_language = "ru"
        translation = translator.translate(message.text, dest=dest_lang, src=source_language)

    await bot.send_message(message.chat.id, translation.text)
    if check_user_wiki_enabled(message):
        await wiki_message(bot, message, translation, dest_lang, source_language)


if __name__ == '__main__':
    print("я работаю")
    bot.run()
