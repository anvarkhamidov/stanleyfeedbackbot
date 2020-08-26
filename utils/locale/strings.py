import os
import json
import yaml
# import app.utils.core as core

_texts = {}
_languages = []


def load_all_languages():
    """Load all language files"""
    current_directory = os.path.dirname(os.path.realpath(__file__))
    language_directory = 'language'
    language_directory_path = os.path.join(current_directory, language_directory)

    for filename in os.listdir(language_directory_path):
        if filename.endswith(".yaml"):
            lang_id = filename.replace('.yaml', '')
            if lang_id not in _languages:
                _languages.append(lang_id)
            if lang_id in _texts:
                continue
            file_path = os.path.join(language_directory_path, filename)
            with open(file=file_path, mode='r', encoding="utf-8") as data:
                _texts[lang_id] = yaml.load(data, Loader=yaml.FullLoader)


def get_all_languages():
    """Get a list of supported languages"""
    if not _languages:
        load_all_languages()
    return _languages


def get_text(key, language, format_str=True):
    """Provides simple translation lookup"""

    def remove_format(text):
        """Remove markdown text formatting from string"""
        return text.replace('`', '').replace('_', '').replace('*', '')

    if not _texts:
        load_all_languages()

    # try to access key for requested language
    if language in _texts and key in _texts[language]:
        if format_str:
            return _texts[language][key]
        else:
            return remove_format(_texts[language][key])

    # fallback to english if translation in requested language does not exist
    elif key in _texts['ru']:

        # construct bug report for devs
        report_text = f"{get_emoji('bug')} <b>Bug Report</b>\n\n" \
                      f"No translation found for key <code>{key}</code> in <code>{language}</code>."
        # core.notify_devs(report_text)

        if format_str:
            return _texts['ru'][key]
        else:
            return remove_format(_texts['ru'][key])

    # construct bug report for devs
    report_text = f"{get_emoji('bug')} <b>Bug Report</b>\n\n" \
                  f"Could not find text for key <code>{key}</code> in <code>{language}</code>."
    # core.notify_devs(report_text)

    # no translation available
    return "Text not found."


def get_all_texts(language):

    def remove_format(text):
        """Remove markdown text formatting from string"""
        return text.replace('`', '').replace('_', '').replace('*', '')

    if language in _texts:
        return _texts[language]


def get_emoji(emoji):
    offset = 127462 - ord('A')

    def flag(code):
        return chr(ord(code[0]) + offset) + chr(ord(code[1]) + offset)

    emojis = {
        "language": "🈯️",
        "language_uz": flag('UZ'),
        "language_ru": flag('RU'),
        "language_en": flag('US'),
        # "overview": "🎮",
        "overview": "🏬",
        "area": "🌎",
        "manager": "🤵",
        "map": "🗺",
        "envelope": "📨",
        "location": "📍",
        "radius": "📏",
        "quest": "📜",
        "pokemon": "🐾",
        "cart": "🛒",
        "pockets": "🛍",
        "shiny": "✨",
        "item": "🍇",
        "task": "🔖",
        "hunt": "🎯️",
        "continue": "➡️",
        "right": "▶️",
        "left": "◀️",
        "reset": "🔄",
        "defer": "⏱",
        "enqueue": "📤",
        "folder": "📁",
        "finish": "🏁",
        "congratulation": "🏆",
        "settings": "⚙️",
        "alert": "⏰",
        "info": "ℹ️",
        "warning": "⚠️",
        "back": "🔙",
        "cancel": "❌",
        "checked": "✅️",
        "trash": "🗑",
        "thumb_up": "👍",
        "thumb_down": "👎",
        "privacy": "👁",
        "tos": "📃",
        "contact": "💬",
        "payment_bag": "💼",
        "card": "💳",
        "cash": "💴",
        "add": "➕",
        "remove": "➖",
        "inbox": "📥",
        "bug": "👻",
        "restart": "🔄",
        "git_pull": "⬇️",
        "question_mark": "❓", 
        "filebox": "🗂",
        "new": "🗞",
    }

    if emoji not in emojis:
        # construct bug report for devs
        text = f"{get_emoji('bug')} <b>Bug Report</b>\n\n" \
               f"The emoji named <code>{emoji}</code> could not be found."
        # core.notify_devs(text)

    return emojis.get(emoji, emojis.get('question_mark', '?'))


