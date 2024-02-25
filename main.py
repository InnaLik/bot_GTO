import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
            repeat = 1
            while repeat != 0:
                d = con.execute(f'select phrase from phrase order by random() limit 1')
                answer = d.fetchone()[0]
                e = con.execute(f"Select count(*) from repeat where phrase = '{answer}'")
                repeat = e.fetchone()[0]
            con.execute(f"Insert into repeat(phrase) values ('{answer}')")
            con.commit()
        await message.answer(answer)

def delete_repeat():
    with sqlite3.connect('database.db') as con:
        con.execute('delete from repeat')
        con.commit()


async def main() -> None:
    bot = Bot(TOKEN)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(delete_repeat, trigger='cron', hour=6, minute=1)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.basicConfig(level=logging.INFO, filename='py_log.txt', filemode='w')

    asyncio.run(main())


