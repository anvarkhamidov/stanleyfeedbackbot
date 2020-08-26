from aiogram import types, md

from utils.database.models import User
import utils.locale.strings as locale


async def get_phone_number(message: types.Message):
    return (await User.filter(user_id=message.from_user.id).values('phone_number'))[0]['phone_number']


async def register(message: types.Message) -> User:
    user = await User.filter(user_id=message.from_user.id).get_or_none()
    msg_dict = dict(message.from_user)
    if not user:
        try:
            msg_dict['user_id'] = msg_dict.pop('id')
            user: User = User(**msg_dict)
            user.phone_number = message.contact.phone_number if message.contact else None # await get_phone_number(message)
            await user.save()
        except Exception as e:
            await message.answer(text=f"DBERROR: {e}")
    else:
        for key, value in msg_dict.items():
            try:
                setattr(user, key, value)
                # print(key, value)
            except Exception as e:
                logging.exception(e)
                continue
    return user
    

async def get_locale(message: types.Message):
    user = await User.filter(user_id=message.chat.id).get_or_none()
    return user.lang if user.lang else 'ru' 


async def show_user_info(message: types.Message):
    user: User = await register(message)
    return await message.answer(md.text(
        md.text('Information about ' + message.from_user.first_name + ' ' + str(message.from_user.last_name)),
        md.text('🔸', md.hbold('Your ID:'), md.hcode(message.from_user.id)),
        md.text('🔸', md.hbold('First name:'), md.hcode(message.from_user.first_name)),
        md.text('🔸', md.hbold('Second name:'), md.hcode(message.from_user.last_name or 'Unknown')),
        md.text('🔸', md.hbold('Username:'), md.hcode(message.from_user.username or 'Unknown')),
        md.text('🔸', md.hbold('Phone number:'), md.hcode(user.phone_number)) if user else "",
        sep='\n',
    ), reply_markup=types.ReplyKeyboardRemove())


async def send_menu_msg(message: types.Message):
    language = await get_locale(message)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=locale.get_text('btn_feedback', language), callback_data="menu:feedback:start")],
        [types.InlineKeyboardButton(text=locale.get_text('btn_settings', language), callback_data="menu:settings")]
    ])
    text = md.text(locale.get_text('msg_feedback', language))
    return text, keyboard