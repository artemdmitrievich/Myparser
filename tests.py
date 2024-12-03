# from Parsers.Main_info_crypto_parser import Additional_CoinGecko_info

# print(Additional_CoinGecko_info().get_popular_crypto())
# print(Additional_CoinGecko_info().get_greatest_growth_crypto())

import sqlite3

conn = sqlite3.connect("Data_base.db")
cursor = conn.cursor()

cursor.execute(
    f"DELETE FROM users_demo_account WHERE Id = ?",
    (537334374,),
)

cursor.execute(
    f"DELETE FROM users_tracking WHERE Id = ?",
    (537334374,),
)

# cursor.execute(
#     f"DELETE FROM users_main_info WHERE Id = ?",
#     (1270674543,),
# )

# cursor.execute(
#     f"DROP TABLE IF EXISTS users_main_info"
# )

# cursor.execute(
#     """
#     INSERT OR IGNORE INTO users_main_info (
#     Id, username, first_name, last_name, is_bot,
#     is_premium, language_code, url
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
#     (
#         2100911465,
#         "egorandr112",
#         "Egor_Andrianow",
#         None,
#         "False",
#         "False",
#         "ru",
#         "tg://user?id=2100911465",

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
