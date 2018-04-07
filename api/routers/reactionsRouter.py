from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.reactionsController import getStoryReactions, addNewReaction, removeReaction
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.get_password
def get_token(username):
    return loginedUsers.checkUserLogin(username)



class ReactionsRouter(Resource):

	@auth.login_required
	def get(self):
		return getStoryReactions(request)

	@auth.login_required
	def put(self):
		return addNewReaction(request)

	@auth.login_required
	def delete(self):
		return removeReaction(request)

		
