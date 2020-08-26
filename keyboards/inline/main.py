from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import utils.locale.strings as locale


# language keyboard
languages = locale.get_all_languages()
keyboard = []
row = []
for lang_id in languages:
    row.append(InlineKeyboardButton(text=f"{locale.get_emoji(f'language_{lang_id}')} "
                                         f"{locale.get_text(f'language_{lang_id}', lang_id)}",
                                    callback_data=f'main:lang:{lang_id}'))
    if len(row) == 2:
        keyboard.append(row)
        row = []
if row:
    keyboard.append(row)

kb_language = InlineKeyboardMarkup(row_width=2, inline_keyboard=keyboard)
