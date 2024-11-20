import sqlite3


async def on_start_update_data_base():

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
                Id INTEGER PRIMARY KEY,
                stop_flag TEXT,
                tracking_quantity INTEGER,
                coin1_first TEXT,
                coin2_first TEXT,
                short_window_first INTEGER,
                long_window_first INTEGER,
                interval_first INTEGER,
                is_tracking_first TEXT,
                coin1_second TEXT,
                coin2_second TEXT,
                short_window_second INTEGER,
                long_window_second INTEGER,
                interval_second INTEGER,
                is_tracking_second TEXT,
                coin1_third TEXT,
                coin2_third TEXT,
                short_window_third INTEGER,
                long_window_third INTEGER,
                interval_third INTEGER,
                is_tracking_third TEXT
    )
"""
    )
    cursor.execute(
        "SELECT * FROM users"
    )
    items = cursor.fetchall()
    if items:
        for item in items:
            if item[8] == "True":
                cursor.execute(
                    """
                    UPDATE users SET is_tracking_first = ? WHERE Id = ?""",
                    ("Waiting", item[0]),
                )
                conn.commit()
            
            if item[14] == "True":
                cursor.execute(
                    """
                    UPDATE users SET is_tracking_second = ? WHERE Id = ?""",
                    ("Waiting", item[0]),
                )
                conn.commit()
            
            if item[20] == "True":
                cursor.execute(
                    """
                    UPDATE users SET is_tracking_third = ? WHERE Id = ?""",
                    ("Waiting", item[0]),
                )
                conn.commit()

    conn.close()