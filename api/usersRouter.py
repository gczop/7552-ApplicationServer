from flask_restful import Resource
import string
import random
from flask import request

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from databases.users import *

class UserRouter(Resource):
	def get(self):
		userInfo = authenticate_user(token= request.headers["token"],email= request.headers["email"],password= request.headers["password"]) 
		if(userInfo == None):
			token = loginUser(request.headers["email"])
			return "Token creado " + token
		return {"message":"Bienvenido {}".format(userInfo["email"]), "token":userInfo["app_token"]}
		

def loginUser(email):
	token = id_generator()
	userCollection.insert_one({
		"email":email,
		"app_token": token
		})
	return token


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
