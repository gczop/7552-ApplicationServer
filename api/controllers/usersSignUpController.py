import os
import string
import random
import json
from databases.loginedUsers import loginedUsers
from logger.log import *

if 'TEST_ENV' in os.environ:
	from mockups.requests.usersSignUpMockUp import *
	from mockups.requests.usersLogInMockUp import *
else:
	from SharedServerRequests.userSignUp import *
	from SharedServerRequests.userLogin import authenticateUserLogin

from databases.users import usersDb


def authenticateSignUp(request):
	user,password,fbToken,personalInfo = getRequestData(request)
	logDebug("usersSignUpController- Authenticating sign up for new user: "+str(user))
	response = registerNewUser(user, password, fbToken);# {"id":4,"_rev":null,"applicationOwner":"String","username":null};
	print (response.text)
	if (response.status_code == 401):
			return {"Error": "Authentication not correct"}, 401
	signUpResponse = json.loads(response.text)
	if(response.status_code != 200):
		logDebug("usersSignUpController- Error while registering user:"+str(signUpResponse))
		logErrorCode("API01", str(signUpResponse["message"]))
		return {"Error": "(Error code: 1)", "Message":signUpResponse["message"]}, 401
	else:
		logDebug("usersSignUpController- New user registered in DB")
		fbUser = False
		if(fbToken):
			fbUser = True
		sentPassword = password or fbToken
		response = authenticateUserLogin(user,sentPassword)
		loginResponse = json.loads(response.text)
		if(response.status_code != 200):
			logDebug("usersSignUpController- Error while loading information:"+str(loginResponse))
			logErrorCode("API01", str(loginResponse["message"]))
			return {"Error": loginResponse['message'] + "(Error code: 41)"}, response.status_code
		else:
			logDebug("usersSignUpController- "+str(personalInfo))
			usersDb.addNewUser(user,loginResponse["token"],personalInfo,fbUser)
			loginedUsers.userLogin(user,loginResponse["token"])
			return {"Message": "Bienvenido {}".format(user), "Token":loginResponse["token"]}	
		



def getRequestData(request):
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

	
