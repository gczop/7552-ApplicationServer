from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.friendsController import getUserFriends, removeFriend
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers






class PingRouter(Resource):


	def get(self):
		return getUserFriends(request)


	def delete(self):
		return removeFriend(request)

		