import random
import sqlite3

from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("menu.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
               "photo TEXT, name TEXT,"
               "description TEXT, price INTEGER)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES "
                       "(?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    random_user = random.choice(result)
    await bot.send_photo(message.from_user.id, random_user[1],
                         caption=f"Name: {random_user[2]}\n"
                                 f"Description: {random_user[3]}\n"
                                 f"Price: {random_user[4]}\n")


async def sql_command_all():
    return cursor.execute("SELECT * FROM anketa").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM anketa WHERE id == ?", (id, ))
    db.commit()


async def sql_commands_get_all_id():
    return cursor.execute("SELECT id FROM anketa").fetchall()
