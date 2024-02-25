from aiogram import Bot

def delete_phrase():
    with sqlite3.connect('database.db') as con:
        con.execute('delete from repeat')
        con.commit()
