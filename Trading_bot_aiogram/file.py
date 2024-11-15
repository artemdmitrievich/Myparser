import sqlite3, time, asyncio
# from app import send_message
# import time


def Func(bot, send_message):
    while True:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users"
        )
        item = cursor.fetchone()
        if item:
            Id = item[0]
            conn.close()
            asyncio.get_event_loop().run_until_complete(send_message(Id, "fjjfj"))
        else:
            conn.close()

        time.sleep(5)
