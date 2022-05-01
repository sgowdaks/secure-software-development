import sqlite3
from flask import g

def validate_userId(userId):
    try:
        con = sqlite3.connect('user_details.db')
        cur = con.cursor()
        cur.execute('''
            SELECT userId FROM users WHERE userId=?''',
            (userId,))
        row = cur.fetchone()
        if row is None:
            return True
        else:
            return False
    finally:
        con.close()

def get_name(userId):
    try:
        con = sqlite3.connect('user_details.db')
        cur = con.cursor()
        cur.execute('''
            SELECT name FROM users WHERE userId=?''',
            (userId,))
        row = cur.fetchone()
        if row is None:
            return None
        else:
            return row
    finally:
        con.close()

def validate_email(email):
    try:
        con = sqlite3.connect('user_details.db')
        cur = con.cursor()
        cur.execute('''
            SELECT * FROM users WHERE email=?''',
            (email,))
        row = cur.fetchone()
        if row is None:
            return True
        else:
            return False
    finally:
        con.close()



def delete_data(userId):
    try:
        # print("yes, deleteing")
        con = sqlite3.connect('user_details.db')
        cur = con.cursor()
        cur.execute('''
                DELETE FROM users WHERE userId=?''',
                (userId,))
        con.commit()
    finally:
        con.close()


def verify_user_amount(source_a, amount, desti_a, target, user):
    try:
        con = sqlite3.connect(source_a+".db")
        cur = con.cursor()
        i = False
        if source_a == "saving_account":
            cur.execute('''
                    SELECT balance FROM saving_account WHERE owner=?''',
                    (user,))
            row = cur.fetchone()
            print("hello")
            row = list(row)
            print(row[0])
            if int(amount) > int(row[0]):
                return False
            else:
                # k = int(row[0]) - int(amount)
                # print("amount to be trasfered: ",k, user)
                cur.execute('''
                        UPDATE saving_account set balance = balance - ? WHERE owner=?''',
                        (int(amount), user))
                if source_a != desti_a:
                    i = True
                    con2 = sqlite3.connect(desti_a+".db")
                    cur2 = con2.cursor()
                else:
                    cur2 = cur
                if desti_a == "saving_account":
                    print("hmm 2nd person")
                    cur2.execute('''
                    SELECT balance FROM saving_account WHERE owner=?''',
                    (target,))
                    row = cur2.fetchone()
                    if row == None:
                        return False
                    row = list(row)
                    cur2.execute('''
                            UPDATE saving_account set balance = balance + ? WHERE owner=?''',
                            (int(amount), target))
                else:
                    cur2.execute('''
                    SELECT balance FROM check_account WHERE owner=?''',
                    (target,))
                    row = cur2.fetchone()
                    if row == None:
                        return False
                    cur2.execute('''
                            UPDATE check_account set balance=balance + ? WHERE owner=?''',
                            (int(amount), target))
                if i == True:
                    con2.commit()
                    con2.close()
                con.commit()
                con.close()
                return True            
        else:
            cur.execute('''
                    SELECT balance FROM check_account WHERE owner=?''',
                    (user,))
            row = cur.fetchone()
            row = list(row)
            if int(amount) > int(row[0]):
                return False
            else:
                cur.execute('''
                        UPDATE check_account set balance = balance - ? WHERE owner=?''',
                        (int(amount), user))
                if source_a != desti_a:
                    i = True
                    con2 = sqlite3.connect(desti_a+".db")
                    cur2 = con2.cursor()
                else:
                    cur2 = cur
                if desti_a == "check_account":
                    # print("hmm 2nd person")
                    cur2.execute('''
                    SELECT balance FROM chcek_account WHERE owner=?''',
                    (target,))
                    row = cur2.fetchone()
                    if row == None:
                        return False
                    row = list(row)
                    cur2.execute('''
                            UPDATE chcek_account set balance = balance + ? WHERE owner=?''',
                            (int(amount), target))
                else:
                    # print("target name: ", target)
                    cur2.execute('''
                    SELECT balance FROM saving_account WHERE owner=?''',
                    (target,))
                    row = cur2.fetchone()
                    if row == None:
                        return False
                    cur2.execute('''
                            UPDATE saving_account set balance=balance + ? WHERE owner=?''',
                            (int(amount), target))
                if i == True:
                    con2.commit()
                    con2.close()
                con.commit()
                con.close()
                return True            
           
    finally:
        con.close()

