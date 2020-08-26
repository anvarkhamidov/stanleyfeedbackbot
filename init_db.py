from tortoise import Tortoise, run_async


async def init():
    await Tortoise.init(
        db_url='postgres://postgres:postgres11@localhost/feedbackbot',
        modules={'models': ['utils.database.models']}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())