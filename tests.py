# from Parsers.Main_info_crypto_parser import Additional_CoinGecko_info

# print(Additional_CoinGecko_info().get_popular_crypto())
# print(Additional_CoinGecko_info().get_greatest_growth_crypto())

import sqlite3

conn = sqlite3.connect("Data_base.db")
cursor = conn.cursor()
cursor.execute(
    "UPDATE users SET tracking_quantity = ? WHERE Id = ?",
    (
        15,
        1270674543,
    ),
)
conn.commit()
conn.close()

conn = sqlite3.connect("Data_base.db")
cursor = conn.cursor()
cursor.execute("SELECT tracking_quantity FROM users")
items = cursor.fetchall()
conn.close()
print(items[0][0])
