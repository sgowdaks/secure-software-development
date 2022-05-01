import sqlite3
from passlib.hash import pbkdf2_sha256

con = sqlite3.connect('saving_account.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE saving_account (
        s_account_no text primary key, owner text, balance integer,
        foreign key(owner) references users(userId))''')
cur.execute(
    "INSERT INTO saving_account VALUES(?, ?, ?)",
    ('100', 'alice',  7500))
cur.execute(
    "INSERT INTO saving_account VALUES(?, ?, ?)",
    ('190', 'bob' , 200))
con.commit()
con.close()