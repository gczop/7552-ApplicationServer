import string
import random
import json
from SharedServerRequests.userSignUp import *
from databases.users import usersDb


def authenticateSignUp(request):
	user,password,fbToken = getRequestData(request)
	response = registerNewUser(user, password, fbToken)
	print (response.text);
	responseData = json.loads(response.text)
	try:
		responseData["code"]
		print(responseData)
		return {"Error": "Login Incorrecto (Error code: 1)"}, 401
	except:
		usersDb.addNewUser(user)
		return {"Message": "Bienvenido {}".format(user)}	


def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	password = data.get("password")
	fbToken = data.get("fbToken")
	return user,password,fbToken