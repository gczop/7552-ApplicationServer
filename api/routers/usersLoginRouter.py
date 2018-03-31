from flask_restful import Resource
from flask import request



from api.controllers.usersLoginController import validateUserLogin


class UsersLoginRouter(Resource):
	def post(self):
		return validateUserLogin(request)


