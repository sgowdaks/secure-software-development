import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import request, g
import jwt
from random import randint
from time import sleep

SECRET = 'bfg28y7efg238re7r6t32gfo23vfy7237yibdyo238do2v3'

#preventing SQL injections using "?", instead of hardcoading
def get_user_with_credentials(email, password):
    try:
        con = sqlite3.connect('user_details.db')
        # print("hello")
        cur = con.cursor()
        cur.execute('''
            SELECT userId, name, password FROM users where email=?''',
            (email,))
        
        row = cur.fetchone()
        if row is None:
            return None
        userId, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            #Preventing of timing attacks
            k = randint(0.1, 2)
            sleep(k)
            print("sleep time :", k)
            return None
        return {"userId": userId, "name": name, "token": create_token(userId)}
    finally:
        con.close()

def logged_in():
    token = request.cookies.get('auth_token')
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        g.user = data['sub']
        return True
    except jwt.InvalidTokenError:
        return False

def create_token(userId):
    now = datetime.utcnow()
    payload = {'sub': userId, 'iat': now, 'exp': now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token

def c_account(userId):
    try:
        con = sqlite3.connect('check_account.db')
        # print("hello")
        cur = con.cursor()
        cur.execute('''
            SELECT c_account_no, balance FROM check_account where owner=?''',
            (userId,))
        
        row = cur.fetchone()
        if row is None:
            return None
        # print(row)
        number, balance = row
        # print("check balance : ", balance)
        # print("check  account: ", number)
        return { "balance": balance , "number": number}
    finally:
        con.close()

def s_account(userId):
    try:
        con = sqlite3.connect('saving_account.db')
        # print("hello")
        cur = con.cursor()
        cur.execute('''
            SELECT s_account_no, balance FROM saving_account where owner=?''',
            (userId,))
        
        row = cur.fetchone()
        if row is None:
            return None
        number, balance = row
        # print("save balance : ", balance)
        # print("save account: ", number))
        return { "balance": balance , "number" : number}
    finally:
        con.close()


