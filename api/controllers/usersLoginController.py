
import json
from flask import request
import os,sys,inspect
from databases.users import usersDb
from databases.loginedUsers import loginedUsers
from logger.log import *

if 'TEST_ENV' in os.environ:
	from mockups.requests.usersLogInMockUp import *
else:
	from SharedServerRequests.userLogin import authenticateUserLogin


def validateUserLogin(request):
		user,password,fbToken = getRequestData(request)
		logDebug("usersLoginController- Validating login for user "+str(user))
		if(password == None and fbToken == None):
			logErrorCode("API02")
			return {"Error": "Falta de informacion de login (Error code: 2)"}, 400
		if(password != None):
			response = authenticateUserLogin(user,password)
		else:
			response = authenticateUserLogin(user,fbToken)
		logDebug("usersLoginController- LoginController - response status:" +str(response.status_code))
		if (response.status_code == 401):
			return {"Error": "Authentication not correct"}, 401
		responseData = json.loads(response.text)
		if (response.status_code != 200):
			logDebug("usersLoginController- "+str(responseData))
			logErrorCode("API03", responseData['message'])
			return {"Error": responseData['message'] + "(Error code: 3)"}, response.status_code
		else:
			logDebug("usersLoginController- Succesful login for user "+str(user))
			usersDb.registerUserToken(user,responseData["token"])
			loginedUsers.userLogin(user,responseData["token"])
			return {"Message": "Bienvenido {}".format(user), "Token":responseData["token"]}	



def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	password = data.get("password")
	fbToken = data.get("fbToken")
	return user,password,fbToken
