from flask_restful import Resource
import string
import random
import json
from flask import request

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from SharedServerRequests.userSignUp import *
from databases.users import *

class UsersSignupRouter(Resource):
	def post(self):
		data = json.loads(request.data)
		user = data.get("username")
		password = data.get("password")
		fbToken = data.get("fbToken")
		response = registerNewUser(user, password, fbToken)
		responseData = json.loads(response.text)
		try:
			responseData["code"]
			return {"Error": "Login Incorrecto"}, 401
		except:
			return {"Message": "Bienvenido {}".format(user)}	

