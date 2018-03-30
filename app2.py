from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_api import status
from json import dumps
from flask import request
from flask import Response
import sys
print (sys.argv[1])

app = Flask(__name__)

# see https://flask-httpauth.readthedocs.io/en/latest/
auth = HTTPBasicAuth()

users = {
    "admin": "root",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/secret')
@auth.login_required
def secret_page():
    return "Hello, %s!" % auth.username()

@app.route('/')
def hello_world():
    return "Hi, I'm root!"


if __name__ == '__main__':
	app.run(port=int(sys.argv[1]))
