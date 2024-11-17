import sqlite3
from multiprocessing import Process
from time import sleep
from Kraken_aio import MovingAverageCrossover


def StartTrackingCrypto():
    while True:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users"
        )
        items = cursor.fetchall()
        if items:
            for item in items:
                if item[2] == 1 and item[8] == "False":
                    cursor.execute(
                        """
                        UPDATE users SET is_tracking_first = ? WHERE Id = ?""",
                        ("True", item[0]),
                    )
                    conn.commit()
                    conn.close()
                    curr = MovingAverageCrossover(item[0], item[3], item[4], item[5], item[6], item[7])
                    curr_f = curr.run
                    process = Process(target=curr_f)
                    process.start()
                else:
                    conn.close()
        else:
            conn.close()
        sleep(5)