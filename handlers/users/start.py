from aiogram import md, types
from aiogram.dispatcher.filters import builtin, state
from aiogram.dispatcher import FSMContext
import utils.locale.strings as locale

from keyboards import inline, default
from loader import dp
from utils.database.models import User
from utils.misc import core, user as fuser
import logging


class UserRegister(state.StatesGroup):
    language = state.State()
    contact = state.State()


async def show_menu(message: types.Message, user: User):

    await message.answer(text=md.text(
        md.text('Information about ' + message.from_user.first_name + ' ' + str(message.from_user.last_name)),
        md.text('🔸', md.hbold('Your ID:'), md.hcode(user.user_id)),
        md.text('🔸', md.hbold('First name:'), md.hcode(user.first_name)),
        md.text('🔸', md.hbold('Second name:'), md.hcode(user.last_name or 'Unknown')),
        md.text('🔸', md.hbold('Username:'), md.hcode(user.username or 'Unknown')),
        md.text('🔸', md.hbold('Phone number:'), md.hcode(user.phone_number)),
        sep='\n',
    ), reply_markup=types.ReplyKeyboardRemove())

    text, keyboard = await fuser.send_menu_msg(message)
    return await message.answer(text=text, reply_markup=keyboard)


# @dp.callback_query_handler(lambda call: call.split(':') == ["menu", "cancel"])


@dp.message_handler(builtin.CommandStart())
async def bot_start(message: types.Message):
    query = await fuser.register(message)

    if not query.lang:
        languages = locale.get_all_languages()
        languages_title = []
        for lang_id in languages:
            languages_title.append(locale.get_text('language', lang_id))

        title = " | ".join(languages_title)
        text = f"{locale.get_emoji('language')} <b>{title}</b>\n\n"

        for lang_id in languages:
            text += f"{locale.get_emoji(f'language_{lang_id}')} {locale.get_text('language_choose', lang_id)}\n"

        await UserRegister.language.set()
        return await message.answer(text=text, reply_markup=inline.kb_language)

    return await show_menu(message, query)


# language setting callback_query_handler
@dp.callback_query_handler(lambda c: c.data.split(':')[-1] in locale.get_all_languages() and str(c.data.split(':')[0]) == "main", 
                           state=UserRegister.language)
async def process_callback_queries(call: types.CallbackQuery, state: FSMContext):
    # lambda callback: callback.data in
    language = call.data.split(':')[-1]
    await call.answer(text=locale.get_text('language_set', language))
    await call.message.delete()

    keyboard = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text=locale.get_text('btn_request_contact', language), request_contact=True)]
    ], one_time_keyboard=True, resize_keyboard=True, row_width=1)

    await call.message.answer(text=f"{locale.get_text('msg_request_contact', language)}",
                              reply_markup=keyboard)
    async with state.proxy() as data:
       data['lang'] = language
    await UserRegister.next()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegister.contact)
async def get_contact(message: types.Message, state: FSMContext):
    language = (await state.get_data())['lang']
    if not await builtin.IsSenderContact(True).check(message):
        return await message.reply(text=f"{locale.get_emoji('warning')} {locale.get_text('not_you', language=language)}",
                                   reply_markup=default.contact_kb)

    try:
        query = await User.filter(user_id=message.chat.id).get_or_none()
        if query:
            query.lang = language
            query.phone_number = message.contact.phone_number
            print(query.lang, query.phone_number)
            await query.save(force_update=True)
            await show_menu(message, query)
            await state.finish()
    except Exception as e:
        core.notify_devs(e)
        logging.exception(e)
    


# remove user from database
@dp.message_handler(commands=['remove'])
async def remove_from_dbb(message: types.Message):
    print(message.chat.id)
    user = await User.filter(user_id=message.chat.id).get_or_none()
    if user:
        await user.delete()