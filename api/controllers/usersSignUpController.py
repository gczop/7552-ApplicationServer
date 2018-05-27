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
	if (response.status_code == 401):
			return {"Error": "Authentication not correct"}, 401
	signUpResponse = json.loads(response.text)
	if(response.status_code != 200):
		print(signUpResponse)
		return {"Error": "(Error code: 1)", "Message":signUpResponse["message"]}, 401
	else:
		sentPassword = password or fbToken
		response = authenticateUserLogin(user,sentPassword)
		loginResponse = json.loads(response.text)
		if(response.status_code != 200):
			print(loginResponse)
			return {"Error": loginResponse['message'] + "(Error code: 41)"}, response.status_code
		else:
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

	