from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.friendsController import getUserFriends, removeFriend, getSpecificUserFriends
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return loginedUsers.checkUserLogin(username,password)



class FriendsRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserFriends(request)

	@auth.login_required
	def delete(self):
		return removeFriend(request)

		
class SpecificUserFriendsRouter(Resource):

	@auth.login_required
	def get(self, username):
		print("Estamos aca")
		return getSpecificUserFriends(username)


		