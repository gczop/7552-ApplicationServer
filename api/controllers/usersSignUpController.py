import os
import string
import random
import json


if 'TEST_ENV' in os.environ:
	from mockups.requests.usersSignUpMockUp import *
else:
	from SharedServerRequests.userSignUp import *

from databases.users import usersDb


def authenticateSignUp(request):
	user,password,fbToken = getRequestData(request)
	response = registerNewUser(user, password, fbToken);# {"id":4,"_rev":null,"applicationOwner":"String","username":null};
	print (response.text)
	responseData = json.loads(response.text)
	try:
		responseData["code"]
		print(responseData)
		return {"Error": "(Error code: 1)", "Message":responseData["message"]}, 401
	except:
		usersDb.addNewUser(user)
		return {"Message": "Bienvenido {}".format(user)}	


def getRequestData(request):
	print("SIGN UP")
	print(request.data)
	data = json.loads(request.data)
	user = data.get("username")
	password = data.get("password")
	fbToken = data.get("fbToken")
	return user,password,fbToken