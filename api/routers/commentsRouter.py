from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.commentsController import getStoryComments, addNewComment, removeComment
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return usersDb.checkUserLogin(username,password)



class CommentsRouter(Resource):

	@auth.login_required
	def get(self):
		return getStoryComments(request)

	@auth.login_required
	def put(self):
		return addNewComment(request)

	@auth.login_required
	def delete(self):
		return removeComment(request)

		
