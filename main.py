from apscheduler.schedulers.asyncio import AsyncIOScheduler
from secret_key import bot_gto
from aiogram import Bot, Dispatcher, types
import asyncio
import sqlite3
import logging
from aiogram.types import FSInputFile, InputFile

TOKEN = bot_gto
dp = Dispatcher()
bot = Bot(TOKEN)

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
        # все названия картинок в бд + такой же словарь без повторений + на выбор либо фото, либо текст
        photo = FSInputFile(path=f'C:/Users/Инна/PycharmProjects/bot_GTO/image/2.png',  filename='2.png')
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
