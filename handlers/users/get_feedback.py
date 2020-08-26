from aiogram import md, types
import utils.locale.strings as locale
from loader import dp
from utils.misc.user import get_locale, send_menu_msg
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FeedbackProcess(StatesGroup):
    intro = State()


@dp.callback_query_handler(lambda c: str(c.data.split(':')[-1]) == "cancel", state="*")
async def main_menu_msg(call: types.CallbackQuery, state: FSMContext):
    if call.data.split(':')[0] == "menu":
        text, keyboard = await send_menu_msg(call.message)
        await state.finish()
        return await call.message.edit_text(text=text, reply_markup=keyboard)


# get user feedback
@dp.callback_query_handler(lambda c: c.data.split(':')[-2:] == ["feedback", "start"])
async def get_feedback(call: types.CallbackQuery):
    # print(call.data.split(':'))
    message = call.message
    language = await get_locale(message)
    await FeedbackProcess.intro.set()
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=locale.get_text('btn_cancel', language), callback_data="menu:cancel")]
    ])
    await message.edit_text(text=md.text(locale.get_text('msg_send_your_feedback', language)), reply_markup=keyboard)


@dp.message_handler(state=FeedbackProcess.intro)
async def handle_feedback_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply(text=message.text)
    await state.finish()
