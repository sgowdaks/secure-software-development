# secure-software-development

## Amaze Pay

>source code is in [flask_web_security](flask_web_security/)

Amaze pay is a mini bank account. It allow users to signup, and login if they already have their account in the bank, and also allows user to transfer money, if the target has account in amaze pay. All of these acts are carried on securly defending CSRF, SQl injection attacks in flask.

### To get started:

1. create a virtual environment: python3 -m venv env
2. eneter the virtual envirnoment: . env/bin/activate
3. Install four libraries: pip install Flask Flask-WTF PyJWT passlib.
4. Add the environment variable: export FLASK_ENV=development (to enable automatic server restart after code changes)

Inorder to access the email verification services, update the email and password.
