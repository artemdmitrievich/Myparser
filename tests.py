# from Parsers.Main_info_crypto_parser import Additional_CoinGecko_info

# print(Additional_CoinGecko_info().get_popular_crypto())
# print(Additional_CoinGecko_info().get_greatest_growth_crypto())

# import sqlite3

# conn = sqlite3.connect("Data_base.db")
# cursor = conn.cursor()

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
#     is_auto_operation, operation_percent,
#     stop_loss_percent, take_profit_percent
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
#     (
#         6236721920,
#         "True",
#         100000,
#         79749.9806037034,
#         "True",
#         20,
#         None,
#         None

#     ),
# )

# cursor.execute(
#     """UPDATE users_demo_account SET start_sum = ?, current_sum = ?,
#     operation_percent = ? WHERE Id = ?
#     """,
#     (
#         999,
#         1911,
#         10,
#         2100911465,
#     ),
# )

# cursor.execute(
#     """UPDATE users_demo_account SET is_demo_account = ? WHERE Id = ?
#     """,
#     (
#         "True",
#         764913946,
#     ),
# )

# cursor.execute(
#     """
#     INSERT OR IGNORE INTO users_demo_account (
#     Id, is_demo_account, start_sum, current_sum,
#     is_auto_operation, operation_percent,
#     stop_loss_percent, take_profit_percent
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
#     (
#         1270674543,
#         "False",
#         0,
#         0,
#         "False",
#         0,
#         None,
#         None

#     ),
# )

# cursor.execute(
#     "UPDATE users_main_info SET url = ? WHERE Id = ?",
#     ("t.me/denis9F", 6236721920,),
# )

# conn.commit()
# conn.close()

# conn = sqlite3.connect("Data_base.db")
# cursor = conn.cursor()
# cursor.execute("SELECT tracking_quantity FROM users")
# items = cursor.fetchall()
# conn.close()
# print(items[0][0])

# stroka = input("Введите строку")
# new = ""
# for i in stroka:
#     if i == "0":
#         new += "1"
#     elif i == "1":
#         new += "0"
#     else:
#         new += i
# print(new)

# import krakenex
# response = krakenex.API().query_public("Ticker", {"pair": "XRP" + "USD"})

# print(float(response["result"][list(response["result"].keys())[0]]["c"][0]))