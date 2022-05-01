import sqlite3
from passlib.hash import pbkdf2_sha256
#using secure password hashing
def add_new_details(userId, name, email, password):
    con = sqlite3.connect('user_details.db')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        (userId, name, email, pbkdf2_sha256.hash(password)))
    con.commit()
    con.close()
