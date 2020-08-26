from loader import bot, storage
from tortoise import Tortoise
import os

WEBHOOK_HOST = 'https://stanleyfeedbackbot.herokuapp.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.environ.get('PORT')

DB_HOST=os.environ.get('DB_HOST')
DB_USER=os.environ.get('DB_USER')
DB_NAME=os.environ.get('DB_NAME')
DB_PASS=os.environ.get('DB_PASS')
DB_PORT=os.environ.get('DB_PORT')
DB_URI = os.environ.get('DATABASE_URL')


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    await Tortoise.init(
        db_url=DB_URI,
        modules={'models': ['utils.database.models']}
    )
    await Tortoise.generate_schemas(safe=True)

    # from utils.notify_admins import on_startup_notify
    # await on_startup_notify(dp)


async def on_shutdown(dp):
    await bot.set_webhook(WEBHOOK_URL)
    await bot.close()
    await storage.close()
    await Tortoise.close_connections()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                           on_startup=on_startup, on_shutdown=on_shutdown,
                           host=WEBAPP_HOST, port=WEBAPP_PORT)
    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
