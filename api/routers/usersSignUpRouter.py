from flask_restful import Resource

from flask import request

# import os,sys,inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir) 

from api.controllers.usersSignUpController import authenticateSignUp

class UsersSignupRouter(Resource):
	def post(self):
		return authenticateSignUp(request)
		
