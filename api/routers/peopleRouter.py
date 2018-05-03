from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.peopleController import searchForPerson, searchForSinglePerson
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return loginedUsers.checkUserLogin(username,password)



class PeopleRouter(Resource):

	@auth.login_required
	def get(self):
		return searchForPerson(request)

class SinglePeopleRouter(Resource):

	@auth.login_required
	def get(self,username):
		return searchForSinglePerson(username)
		