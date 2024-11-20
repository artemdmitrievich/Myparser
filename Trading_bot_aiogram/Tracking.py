import sqlite3
from multiprocessing import Process
from time import sleep
from Kraken_aio import MovingAverageCrossover


def StartTrackingCrypto():
    while True:
        conn = sqlite3.connect("Data_base.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        items = cursor.fetchall()
        if items:
            for item in items:
                if item[8] == "Waiting":
                    cursor.execute(
                        """
                        UPDATE users SET is_tracking_first = ? WHERE Id = ?""",
                        ("True", item[0]),
                    )
                    conn.commit()
                    curr = MovingAverageCrossover(
                        item[0], "3_4;",item[3], item[4], item[5], item[6], item[7]
                    )
                    curr_f = curr.run
                    process = Process(target=curr_f)
                    process.start()
                elif item[14] == "Waiting":
                    cursor.execute(
                        """
                        UPDATE users SET is_tracking_second = ? WHERE Id = ?""",
                        ("True", item[0]),
                    )
                    conn.commit()
                    curr = MovingAverageCrossover(
                        item[0], "9_10;", item[9], item[10], item[11], item[12], item[13]
                    )
                    curr_f = curr.run
                    process = Process(target=curr_f)
                    process.start()
                elif item[20] == "Waiting":
                    cursor.execute(
                        """
                        UPDATE users SET is_tracking_third = ? WHERE Id = ?""",
                        ("True", item[0]),
                    )
                    conn.commit()
                    curr = MovingAverageCrossover(
                        item[0], "15_16;", item[15], item[16], item[17], item[18], item[19]
                    )
                    curr_f = curr.run
                    process = Process(target=curr_f)
                    process.start()
                sleep(1)
        conn.close()
        sleep(5)
