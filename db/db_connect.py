import sqlite3
from settings import config

conn = sqlite3.connect(config.DB_BASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


async def database():
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS "fuel" (
            "id"	INTEGER NOT NULL UNIQUE,
            "station"	TEXT NOT NULL,
            "fuel_92"	INTEGER DEFAULT 0,
            "fuel_95"	INTEGER DEFAULT 0,
            "fuel_diezel"	INTEGER DEFAULT 0,
            "fuel_gaz"	INTEGER DEFAULT 0,
            "address"	TEXT,
            "link"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
            "id"	INTEGER NOT NULL UNIQUE,
            "user_id"	INTEGER NOT NULL UNIQUE,
            "username"	TEXT DEFAULT NULL,
            "first_name"	TEXT DEFAULT NULL,
            "last_name"	TEXT DEFAULT NULL,
            "full_name"	TEXT DEFAULT NULL,
            "mute_time"	INTEGER DEFAULT 0,
            "ban_time"	INTEGER DEFAULT 0,
            PRIMARY KEY("id" AUTOINCREMENT)
        );""")
        conn.commit()
        print("Успішне підключення до бази данних")
    except Exception as e:
        print(f'Помилка при створенні таблиць \n{e}')


async def update_db(state):
    async with state.proxy() as data:
        if data.get('choise_fuel') is None:
            return
        sql = "UPDATE fuel SET "
        kort = []
        for i in ['fuel_92', 'fuel_95', 'fuel_diezel', 'fuel_gaz']:
            if data['choise_fuel'].get(i) is not None:
                sql += f"{i} = ?, "
                kort.append(data['choise_fuel'].get(i))
        sql = sql[:-2] + ' '
        sql += "WHERE station = ?"
        kort.append(data['station'])
        cursor.execute(sql, tuple(kort))
    conn.commit()


def get_fuel():
    try:
        sql = "SELECT * from fuel"
        cursor.execute(sql)
        station = cursor.fetchall()
        return station
    except Exception as e:
        print(f"Виникла помилка:\nERROR:{e}")


def user_exists(user_id) -> bool:
    sql = "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
    r = cursor.execute(*sql).fetchone()
    return r is not None


def add_users(tg_user):
    try:
        sql = "INSERT INTO users (user_id, username, first_name, last_name, full_name) " \
              "VALUES (?, ?, ?, ?, ?)", tuple(tg_user)
        cursor.execute(*sql)
        conn.commit()
    except Exception as e:
        print(f"Виникла помилка:\nERROR:{e}")


def get_users():
    try:
        sql = "SELECT * from users"
        cursor.execute(sql)
        users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Виникла помилка:\nERROR:{e}")
