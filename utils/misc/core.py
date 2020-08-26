import typing
import logging
from aiogram import Dispatcher

from data.config import admins

_dp: typing.Optional[Dispatcher] = None


def set_dispatcher(dp: Dispatcher):
    """Remember a reference to the dispatcher."""
    global _dp
    _dp = dp


async def notify_devs(text: str):
    for admin in admins:
        try:
            await _dp.bot.send_message(admin, f"[DEV]: {text}")
        except Exception as e:
            logging.exception(e)