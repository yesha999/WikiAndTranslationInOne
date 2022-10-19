from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dest_languages_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Русский", callback_data="ru"),
    InlineKeyboardButton("English", callback_data="en"),
    InlineKeyboardButton("中文", callback_data="zh-cn")],
    [InlineKeyboardButton("Español", callback_data="es"),
     InlineKeyboardButton("العربية", callback_data="ar"),
     InlineKeyboardButton("Português", callback_data="pt")],
    [InlineKeyboardButton("日本語", callback_data="ja"),
     InlineKeyboardButton("Deutsch", callback_data="de"),
     InlineKeyboardButton("Français", callback_data="fr")],
    [InlineKeyboardButton("Изменить язык ввода", callback_data="page_2")]])

src_languages_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Определять автоматически", callback_data="src_auto")],
    [
        InlineKeyboardButton("Русский", callback_data="src_ru"),
        InlineKeyboardButton("English", callback_data="src_en"),
        InlineKeyboardButton("中文", callback_data="src_zh-cn")],
    [InlineKeyboardButton("Español", callback_data="src_es"),
     InlineKeyboardButton("العربية", callback_data="src_ar"),
     InlineKeyboardButton("Português", callback_data="src_pt")],
    [InlineKeyboardButton("日本語", callback_data="src_ja"),
     InlineKeyboardButton("Deutsch", callback_data="src_de"),
     InlineKeyboardButton("Français", callback_data="src_fr")],
    [InlineKeyboardButton("Вернуться", callback_data="page_1")]])
