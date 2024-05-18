import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from app.config import BOT_TOKEN

dp = Dispatcher()

@dp.message()
async def calc_salary(message: Message):
    answer = message.text
    await message.answer(text=answer)

async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())