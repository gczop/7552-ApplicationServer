import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.notifications import notificationsDb
from databases.loginedUsers import loginedUsers

def getUserProfile(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Usuario no especificado en el header (Error code: 19)"}, 400
	return notificationsDb.getUserProfile(username)

def updateUserProfile(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Usuario no especificado en el header (Error code: 20)"}, 400
	personalInfo = getRequestData(request)
	return notificationsDb.updateUserProfile(username,personalInfo)


def getRequestData(request):
	personalInfo = {}
	data = json.loads(request.data)
	personalInfo["firstname"] = data.get("firstname")
	personalInfo["lastname"] = data.get("lastname")
	personalInfo["age"] = data.get("age")
	return personalInfo
