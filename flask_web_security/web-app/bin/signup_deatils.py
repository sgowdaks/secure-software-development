import sqlite3
from passlib.hash import pbkdf2_sha256

con = sqlite3.connect('user_details.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE users (
        userId text primary key, name text, email text, password text)''')
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?, ?)",
    ('alice', 'Alice Xu', 'alice@example.com', pbkdf2_sha256.hash("123456")))
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?, ?)",
    ('bob', 'Bobby Tables', 'bob@example.com', pbkdf2_sha256.hash("123456")))
con.commit()
con.close()