from flask import Flask
from flask_restful import Resource, Api


import json
from flask_httpauth import HTTPBasicAuth
from flask_api import status
from json import dumps
from flask import request
from flask import Response
from api.usersRouter import UserRouter

application = Flask(__name__)

api = Api(application, prefix="/api")

api.add_resource(UserRouter,'/users')

# see https://flask-httpauth.readthedocs.io/en/latest/
# auth = HTTPBasicAuth()

# users = {
#     "admin": "root",
# }

# @auth.get_password
# def get_pw(username):
#     if username in users:
#         return users.get(username)
#     return None

# @application.route('/secret')
# @auth.login_required
# def secret_page():
#     return "Hello, %s!" % auth.username()



@application.route('/')
def hello_world():
    return "Hi, I'm root!"


if __name__ == '__main__':
	application.run(host='0.0.0.0')
