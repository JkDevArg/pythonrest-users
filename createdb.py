import sqlite3
conn = sqlite3.connect('users.db')

cur = conn.cursor()

cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, email TEXT, age INTEGER, country TEXT, genre TEXT, birthday TEXT, phone TEXT)")