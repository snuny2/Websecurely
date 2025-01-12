import sqlite3

conn = sqlite3.connect('pyBook.db')

cursor = conn.cursor()

SQL = 'create table if not exists users (id integer primary key autoincrement, ' \
    'username TEXT NOT NULL, email TEXT NOT NULL, passwd TEXT NOT NULL, authkey TEXT)'

cursor.execute(SQL)

cursor.close()
conn.close()