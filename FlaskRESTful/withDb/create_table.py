import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
cur.execute(create_table)
create_table = "CREATE TABLE IF NOT EXISTS items (name TEXT, price REAL)"
cur.execute(create_table)
conn.commit()
conn.close()
