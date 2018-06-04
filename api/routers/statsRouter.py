from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.statsController import authenticateServer
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers




class StatsRouter(Resource):

	def get(self):
		return getUserFriends(request)

	def delete(self):
		return removeFriend(request)

	def post(self):
		return authenticateServer(request)