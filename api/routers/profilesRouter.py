from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.profilesController import getUserProfile, updateUserProfile
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    a = loginedUsers.checkUserLogin(username,password)
    print(a,'BBBBBB')
    return a



class ProfilesRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserProfile(request)

	@auth.login_required
	def put(self):
		return updateUserProfile(request)

		