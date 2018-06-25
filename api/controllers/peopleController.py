import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.users import usersDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def searchForPerson(request):
	searchedFor = getRequestHeader(request,"searchedFor")
	logDebug("peopleController- Searching for "+str(searchedFor))
	if(searchedFor == None):
		logErrorCode("API04")
		return {"Error": "Falta de informacion en header (Error code: 4)"}, 400
	return {"people": usersDb.searchForUsers(searchedFor)}

def searchForSinglePerson(username):
	user = usersDb.searchForSingleUser(username)
	logDebug("peopleController- Searching for "+str(user))
	if(user == None):
		logErrorCode("API05")
		return {"Error": "Username del usuario incorrecto (Error code: 5)"}, 400
	return { "people": user}
