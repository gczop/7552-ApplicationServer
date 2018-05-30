import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.users import usersDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def searchForPerson(request):
	searchedFor = getRequestHeader(request,"searchedFor")
	log("Searching for "+str(searchedFor))
	if(searchedFor == None):
		logError("API04")
		return {"Error": "Falta de informacion en header (Error code: 4)"}, 400
	return usersDb.searchForUsers(searchedFor)

def searchForSinglePerson(username):
	user = usersDb.searchForSingleUser(username)
	log("Searching for "+str(user))
	if(user == None):
		logError("API05")
		return {"Error": "Username del usuario incorrecto (Error code: 5)"}, 400
	return user
