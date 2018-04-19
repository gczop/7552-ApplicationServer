import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.users import usersDb
from databases.loginedUsers import loginedUsers

def getUserProfile(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Usuario no especificado en el header (Error code: 19)"}, 400
	return usersDb.getUserProfile(username)

def updateUserProfile(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Usuario no especificado en el header (Error code: 20)"}, 400
	personalInfo = getRequestData(request)
	return usersDb.updateUserProfile(username,personalInfo)


def getRequestData(request):
	personalInfo = {}
	data = json.loads(request.data)
	personalInfo["firstname"] = data.get("firstname")
	personalInfo["lastname"] = data.get("lastname")
	personalInfo["age"] = data.get("age")
	personalInfo["gender"] = data.get("gender")
	personalInfo["birthday"] = data.get("birthday")
	print(personalInfo, "En utils")
	return personalInfo
