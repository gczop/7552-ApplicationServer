import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.users import usersDb
from databases.loginedUsers import loginedUsers

def searchForPerson(request):
	searchedFor = request.headers.get("searchedFor")
	if(searchedFor == None):
		return {"Error": "Falta de informacion en header (Error code: 4)"}, 400
	return usersDb.searchForUsers(searchedFor)

def searchForSinglePerson(username):
	user = usersDb.searchForSingleUser(username)
	if(user == None):
		return {"Error": "Username del usuario incorrecto (Error code: 5)"}, 400
	return user
