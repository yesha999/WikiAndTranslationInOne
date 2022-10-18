import os

from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from db_functions import change_user_language, check_user_language, check_user_wiki_enabled, off_wiki_enabled, \
    on_wiki_enabled
from wiki_functions import wiki_message

bot = Client("my_bot", api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))
LANGUAGES = ["ru", "en", "zh-cn", "es", "ar", "pt", "ja", "de", "fr"]
EXCEPTION_LANGUAGES = ["uk", "mn", "be", "ky", "kk", "tg", "mk", "bg"]


@bot.on_message(filters.command("lang") & filters.private)
async def change_language(bot: Client, message: Message):
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


@bot.on_message(filters.command("start") & filters.private)
async def start_bot(bot: Client, message: Message):
    await message.reply_text(
        text=f"Привет **{message.from_user.first_name}** \n\n __Я самый умный и простой Бот-переводчик__")
    await change_language(bot, message)


@bot.on_message(filters.command("offwiki") & filters.private)
async def off_wiki(bot: Client, message: Message):
    off_wiki_enabled(message)
    await bot.send_message(message.from_user.id, "Mode: No Wikipedia")


@bot.on_message(filters.command("onwiki") & filters.private)
async def on_wiki(bot: Client, message: Message):
    on_wiki_enabled(message)
    await bot.send_message(message.from_user.id, "Mode: Wikipedia")


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
        change_user_language(bot, answer_message)
        translator = Translator()
        translation = translator.translate("Язык выбран.", dest=answer_message.data, src='ru')
        await bot.send_message(answer_message.message.chat.id, translation.text)


@bot.on_message(filters.text & filters.private)
async def translate_and_wiki(bot: Client, message: Message):
    lang = check_user_language(message)
    translator = Translator()
    translation = translator.translate(message.text, dest=lang)
    source_language = translation.src
    if source_language in EXCEPTION_LANGUAGES:  # Иногда русский язык определяется как другой язык,
        # Пример: слово "баг" определяется как монгольское и перевод неправильный.
        source_language = "ru"
        translation = translator.translate(message.text, dest=lang, src=source_language)

    await bot.send_message(message.chat.id, translation.text)
    if check_user_wiki_enabled(message):
        await wiki_message(bot, message, translation, lang, source_language)


if __name__ == '__main__':
    bot.run()
