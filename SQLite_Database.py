import sqlite3

connection = sqlite3.connect('bank_accounts.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE bank_accounts (
                 username text,
                 password text,
                 balance float,
                 pin_code int,
                 occupied int )""")


connection.commit()
connection.close()
