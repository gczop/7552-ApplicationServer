from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.profilesController import getUserProfile, updateUserProfile
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import *



auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
	return usersDb.checkUserLogin(username,password)



class ProfilesRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserProfile(request)

	@auth.login_required
	def put(self):
		return updateUserProfile(request)

		