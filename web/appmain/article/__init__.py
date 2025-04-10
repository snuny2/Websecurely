import sqlite3

conn = sqlite3.connect('pyBook.db')
cursor = conn.cursor()

# 테이블 제거
# SQL = 'drop table articles'
# cursor.execute(SQL)

# 상품정보 저장
SQL = 'create table if not exists articles (articleNo integer primary key autoincrement, ' \
    'author text not NULL, title text not NULL, category, integer, description text, \
    price integer, picture text)'

cursor.execute(SQL)

cursor.close()
conn.close()