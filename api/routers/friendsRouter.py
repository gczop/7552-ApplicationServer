from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.friendsController import getUserFriends, addFriend, removeFriend, getSpecificUserFriends
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    a = loginedUsers.checkUserLogin(username,password)
    print(a, username, password)
    return a


class FriendsRouter(Resource):

    @auth.login_required
    def get(self):
        return getUserFriends(request)

    # For testing purposes
    @auth.login_required
    def post(self):
        return addFriend(request)

    @auth.login_required
    def delete(self):
        return removeFriend(request)


class SpecificUserFriendsRouter(Resource):

    @auth.login_required
    def get(self, username):
        print("Estamos aca")
        return getSpecificUserFriends(username)
