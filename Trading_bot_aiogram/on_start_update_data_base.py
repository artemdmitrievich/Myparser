import sqlite3


# Обновление базы данных при запуске бота
async def on_start_update_data_base():

    conn = sqlite3.connect("Data_base.db")
    cursor = conn.cursor()
    # Создаём таблицу "users_tracking"
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users_tracking (
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

    conn.commit()

    # Создаём таблицу "users_demo_account"
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users_demo_account (
                Id INTEGER PRIMARY KEY,
                is_demo_account TEXT,
                start_sum INTEGER,
                current_sum INTEGER,
                is_auto_operation TEXT,
                operation_percent INTEGER
    )
"""
    )

    conn.commit()

    # Убираем стоп сигналы и ставим, отслеживаемые валюты, в очередь ("Waiting")
    cursor.execute("SELECT * FROM users_tracking")
    items = cursor.fetchall()
    if items:
        for item in items:
            if not item[1]:
                item_1 = "None"
            else:
                item_1 = item[1]
            if item[8] == "True" and "3_4;" not in item_1:
                cursor.execute(
                    """
                    UPDATE users_tracking SET is_tracking_first = ? WHERE Id = ?""",
                    ("Waiting", item[0]),
                )
                conn.commit()

            if item[14] == "True" and "9_10;" not in item_1:
                cursor.execute(
                    """
                    UPDATE users_tracking SET is_tracking_second = ? WHERE Id = ?""",
                    ("Waiting", item[0]),
                )
                conn.commit()

            if item[20] == "True" and "15_16;" not in item_1:
                cursor.execute(
                    """
                    UPDATE users_tracking SET is_tracking_third = ? WHERE Id = ?""",
                    ("Waiting", item[0]),
                )
                conn.commit()

            if item[1]:
                cursor.execute(
                    """
                    UPDATE users_tracking SET stop_flag = ? WHERE Id = ?""",
                    (None, item[0]),
                )
                conn.commit()

    conn.close()
