import string
import random
import json
from SharedServerRequests.userSignUp import *
from databases.users import *


def authenticateSignUp(request):
	user,password,fbToken = getRequestData(request)
	response = registerNewUser(user, password, fbToken)
	responseData = json.loads(response.text)
	try:
		responseData["code"]
		return {"Error": "Login Incorrecto"}, 401
	except:
		return {"Message": "Bienvenido {}".format(user)}	

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	password = data.get("password")
	fbToken = data.get("fbToken")
	return user,password,fbToken