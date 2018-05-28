from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.statsController import authenticateServer
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return usersDb.checkUserLogin(username,password)



class StatsRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserFriends(request)

	@auth.login_required
	def delete(self):
		return removeFriend(request)

	def post(self):
		return authenticateServer(request)