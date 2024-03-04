import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from secret_key import bot_gto
from aiogram import Bot, Dispatcher, types
import asyncio
import sqlite3
import logging
from aiogram.types import FSInputFile
import random

TOKEN = bot_gto
dp = Dispatcher()
bot = Bot(TOKEN)


@dp.message()
async def handler_photo(message: types.Message):
    if message.photo:
        s = random.choices(['phrase', 'img'])
        # отправляю либо фразу либо картинку
        if s == ['phrase']:
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
        else:
            # все названия картинок в бд + такой же словарь без повторений + на выбор либо фото, либо текст
            with sqlite3.connect('database.db') as con:
                repeat = 1
                while repeat != 0:
                    d = con.execute(f'select path from image order by random() limit 1')
                    answer = d.fetchone()[0]
                    e = con.execute(f"Select count(*) from repeat where phrase = '{answer}'")
                    repeat = e.fetchone()[0]
                con.execute(f"Insert into repeat(phrase) values ('{answer}')")
                con.commit()
            photo = FSInputFile(path=f'{os.getcwd()}/image/{answer}')
            await bot.send_photo(chat_id=message.chat.id, photo=photo)


def delete_repeat():
    with sqlite3.connect('database.db') as con:
        con.execute('delete from repeat')
        con.commit()


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(delete_repeat, trigger='cron', hour=6, minute=1)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.basicConfig(level=logging.INFO, filename='py_log.txt', filemode='w')

    asyncio.run(main())
