from flask_restful import Resource
import string
import random
import json
from flask_httpauth import HTTPBasicAuth
from flask import request



import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers

auth = HTTPBasicAuth()

@auth.get_password
def get_token(username):
    return loginedUsers.checkUserLogin(username)



class FriendsRouter(Resource):

	@auth.login_required
	def post(self):
		return "Has pasado la autenticacion"

def registerUserToken(user, token):
	userCollection.find_one_and_update({"email":user},
		{"$set": {"app_token": "token"}},upsert=True)
