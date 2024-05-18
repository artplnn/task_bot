import asyncio
import json

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from app.config import BOT_TOKEN, logger
from app.constants import ERROR_TEXT
from app.models import FilterSalaryQuery
from app.mongodb import MongoDB
from app.utils import prepare_answer

dp = Dispatcher()

@dp.message()
async def calc_salary(message: Message, client_mongodb: MongoDB):
    try:
        query = json.loads(message.text)
        filter_salary = FilterSalaryQuery(**query)
        data_from_db = client_mongodb.get_data(filter_salary)
        answer = prepare_answer(data_from_db)
        await message.answer(text=answer)
    except Exception:
        logger.exception("Main error")
        await message.answer(text=ERROR_TEXT)


async def main():
    dp["client_mongodb"] = MongoDB()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())