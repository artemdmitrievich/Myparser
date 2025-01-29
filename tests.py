# from Parsers.Main_info_crypto_parser import Additional_CoinGecko_info

# print(Additional_CoinGecko_info().get_popular_crypto())
# print(Additional_CoinGecko_info().get_greatest_growth_crypto())

import sqlite3

conn = sqlite3.connect("Data_base.db")
cursor = conn.cursor()

# cursor.execute(
#     f"DROP TABLE IF EXISTS users_demo_account"
# )

# cursor.execute(
#     f"DELETE FROM users_demo_account WHERE Id = ?",
#     (537334374,),
# )

# cursor.execute(
#     f"DELETE FROM users_tracking WHERE Id = ?",
#     (537334374,),
# )

# cursor.execute(
#     f"DELETE FROM users_main_info WHERE Id = ?",
#     (1270674543,),
# )

# cursor.execute(
#     f"DROP TABLE IF EXISTS users_main_info"
# )

# cursor.execute(
#     """
#     INSERT OR IGNORE INTO users_demo_account (
#     Id, is_demo_account, start_sum, current_sum,
#     is_auto_operation, operation_percent
#     ) VALUES (?, ?, ?, ?, ?, ?)""",
#     (
#         5510002999,
#         "False",
#         0,
#         0,
#         "False",
#         0,

#     ),
# )

# cursor.execute(
#     "UPDATE users_main_info SET url = ? WHERE Id = ?",
#     ("t.me/denis9F", 6236721920,),
# )

conn.commit()
conn.close()

# conn = sqlite3.connect("Data_base.db")
# cursor = conn.cursor()
# cursor.execute("SELECT tracking_quantity FROM users")
# items = cursor.fetchall()
# conn.close()
# print(items[0][0])
