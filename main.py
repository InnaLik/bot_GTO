from secret_key import bot_gto
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio
import sqlite3
import logging

TOKEN = bot_gto
dp = Dispatcher()


@dp.message()
async def handler_photo(message: types.Message):
    if message.photo:
        with sqlite3.connect('database.db') as con:
            d = con.execute(f'select phrase from phrase order by random() limit 1')
            answer = d.fetchone()[0]
        await message.answer(answer)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, filename='py_log.txt', filemode='w')
    asyncio.run(main())

