from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.friendsController import getUserFriends, removeFriend
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.get_password
def get_token(username):
    return loginedUsers.checkUserLogin(username)



class PingRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserFriends(request)

	@auth.login_required
	def delete(self):
		return removeFriend(request)

		