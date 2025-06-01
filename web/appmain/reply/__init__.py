import sqlite3

conn = sqlite3.connect('pyBook.db')
cursor = conn.cursor()

# SQL = 'drop table replies;
#
# cursor.execute(SQL)

SQL = 'create table if NOT exists replies (replyNo integer primary KEY autoincrement, ' \
    'author text NOT NULL, description text NOT NULL, targetArticle integer NOT NULL)'

cursor.execute(SQL)

cursor.close()
conn.close()