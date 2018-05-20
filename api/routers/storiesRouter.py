from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.storiesController import getHomepageFeed, addNewStory, updateStory, removeStory
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return usersDb.checkUserLogin(username,password)



class StoriesRouter(Resource):

	@auth.login_required
	def get(self):
		return getHomepageFeed(request)

	@auth.login_required
	def post(self):
		return addNewStory(request)

	@auth.login_required
	def put(self):
		return updateStory(request)

	@auth.login_required
	def delete(self):
		return removeStory(request)
		