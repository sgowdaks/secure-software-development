from flask import Flask, render_template, request, make_response, render_template, redirect, g
from validation import validate_userId, get_name, validate_email, delete_data, verify_user_amount
from user_service import get_user_with_credentials, logged_in, c_account, s_account
from adding_to_db import add_new_details
from flask_wtf.csrf import CSRFProtect 
from flask_mail import *
from random import *  
import secrets 
import pyotp
import sqlite3



needed = "" 


# k = secrets.randbits(randint(100,500))
# print(k)

con = sqlite3.connect('user_details.db')
cur = con.cursor()

app = Flask(__name__)
mail = Mail(app)



app.config['SECRET_KEY'] = '673783298390384t4578737820938232862731283'
csrf = CSRFProtect(app) 

app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'shivanigowda123ks@gmail.com'  
app.config['MAIL_PASSWORD'] = '****'   #password
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  

mail = Mail(app)  
otp = pyotp.random_base32()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if not logged_in():
            return render_template("login.html")
        return redirect('/dashboard')


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        # print(email)
        # print("hello Shivani")
        password1 = request.form.get("password1")
        userId = request.form.get("userId")
        password2 = request.form.get("password2")
        firstName = request.form.get("firstName")
        #user Id validation 
        response = validate_userId(userId)
        if len(password1) < 7: 
           return render_template("signup.html", error="password very short") 
        if len(password1) > 25:
            return render_template("signup.html", error="password too long") 
        if(password1 != password2):
            return render_template("signup.html", error="password does not match!")
        if response == True:
            res = validate_email(email)
            if res == True:
                add_new_details(userId, firstName, email, password1) 
                # return render_template("login.html")
                msg = Message('OTP',sender = 'shivanigowda123ks@gmail.com', recipients = [email])  
                msg.body = str(otp) 
                mail.send(msg)  
                global needed 
                needed = userId
                print("needed: ", needed)
                return render_template("validate.html")
        return render_template("signup.html", error="Sorry! something went wrong. Try again!")
        


    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        userId = request.form.get("userId")
        password = request.form.get("password")
        #user credentials validation
        user = get_user_with_credentials(userId, password)
        if not user:
            return render_template("login.html", error="Invalid credentials")
        print(user)
        response = make_response(redirect("/dashboard"))
        response.set_cookie("auth_token", user["token"])
        return response, 303
    return render_template("login.html")

    
@app.route("/dashboard", methods=['GET'])
def dashboard():
    if not logged_in():
        return render_template("login.html")
    name = get_name(g.user)
    return render_template("dashboard.html", name = g.user)

@app.route("/saving_details", methods=['GET', 'POST'])
def saving_details():
    if not logged_in():
        return render_template("login.html")
    if s_account(g.user) == None:
        return render_template("saving_details.html", error = "error")
    else:
        res = s_account(g.user)
        return render_template("saving_details.html", balance = res['balance'], number = res['number'])

@app.route("/check_details", methods=['GET', 'POST'])
def check_details():
    if not logged_in():
        return render_template("login.html")
    if c_account(g.user) == None:
        return render_template("check_details.html", error = "error")
    else:
        res = c_account(g.user)
        return render_template("check_details.html", balance = res['balance'], number = res['number'])

@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    #deleting cookie once after logout
    response.delete_cookie('auth_token')
    return response, 303

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")


@app.route('/validate',methods=["POST"])   
def validate():  
    user_otp = request.form['otp']  
    if otp == user_otp:  
        return render_template("login.html")
    else:
        print("global use ",needed)
        delete_data(needed)
        print("calling signup again")
        return render_template("signup.html", error="could not verify the email!")

@app.route("/transfer_money", methods=["POST", "GET"])
def transfer_money():
    if not logged_in():
        return render_template("login.html")
    if request.method == "POST":
        source_a = request.form.get("account_t1")
        desti_a = request.form.get("account_t2")
        target = request.form.get("to")
        amount = request.form.get("amount")
        if int(amount) <= 0:
            return render_template("trasfer_money.html", error = "Please slect the right amount")
        #secure money trasfering
        response = verify_user_amount(source_a, amount, desti_a, target, g.user)
        if response:
            return render_template("trasfer_money.html", error = "Money was succesfully transferred")
        else:
            return render_template("trasfer_money.html", error = "Money trasfer failed")
    return render_template("trasfer_money.html")







