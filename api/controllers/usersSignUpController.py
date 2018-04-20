import os
import string
import random
import json
from databases.loginedUsers import loginedUsers

if 'TEST_ENV' in os.environ:
	from mockups.requests.usersSignUpMockUp import *
	from mockups.requests.usersLogInMockUp import *
else:
	from SharedServerRequests.userSignUp import *
	from SharedServerRequests.userLogin import authenticateUserLogin

from databases.users import usersDb


def authenticateSignUp(request):
	user,password,fbToken,personalInfo = getRequestData(request)
	response = registerNewUser(user, password, fbToken);# {"id":4,"_rev":null,"applicationOwner":"String","username":null};
	print (response.text)
	signUpResponse = json.loads(response.text)
	try:
		signUpResponse["code"]
		print(signUpResponse)
		return {"Error": "(Error code: 1)", "Message":signUpResponse["message"]}, 401
	except:
		sentPassword = password or fbToken
		response = authenticateUserLogin(user,sentPassword)
		loginResponse = json.loads(response.text)
		try:
			loginResponse["code"]
			print(loginResponse)
			return {"Error": "Error inseperado (Error code: 41)"}, 401
		except:
			print(personalInfo)
			usersDb.addNewUser(user,loginResponse["token"],personalInfo)
			loginedUsers.userLogin(user,loginResponse["token"])
			return {"Message": "Bienvenido {}".format(user), "Token":loginResponse["token"]}	
		



def getRequestData(request):
	print("SIGN UP")
	print(request.data)
	data = json.loads(request.data)
	user = data.get("username")
	password = data.get("password")
	fbToken = data.get("fbToken")
	personalInfo={}
	personalInfo["firstname"] = data.get("fisrtname")
	personalInfo["lastname"] = data.get("lastname")
	personalInfo["gender"] = data.get("gender")
	personalInfo["age"] = data.get("age")
	personalInfo["birthday"] = data.get("birthday")
	return user,password,fbToken,personalInfo

	