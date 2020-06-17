import sqlite3

con = sqlite3.connect('list.sqlite')
cursor = con.cursor()
# cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
cursor.execute("SELECT * FROM domain;")
print(cursor.fetchall())