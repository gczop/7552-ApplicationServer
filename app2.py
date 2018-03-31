from flask import Flask
from flask_restful import Resource, Api



from flask_api import status
from api.routers.usersLoginRouter import UsersLoginRouter
from api.routers.usersSignUpRouter import UsersSignupRouter
from api.routers.friendsRouter import FriendsRouter
from api.routers.invitationsRouter import InvitationsRouter

application = Flask(__name__)

api = Api(application, prefix="/api")

api.add_resource(UsersLoginRouter,'/users/login')
api.add_resource(UsersSignupRouter,'/users/signup')
api.add_resource(FriendsRouter,'/friends')
api.add_resource(InvitationsRouter,'/invitations')

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
