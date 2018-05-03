from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.conversationsController import getUserConversations, createNewConversation
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return loginedUsers.checkUserLogin(username,password)



class ConversationsRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserConversations(request)

	@auth.login_required
	def put(self):
		return createNewConversation(request)

		
