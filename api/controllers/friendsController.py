import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.friends import *
from databases.loginedUsers import loginedUsers

def getUserFriends(request):
	username = request.headers.get("username")
	print("AAaaaaa" + username)
	if(username == None):
		return {"Error": "Falta de informacion en header"}, 400
	return DbgetUserFriends(username)

def removeFriend(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header"}, 400
	friend = getRequestData(request)
	if(friend == None):
		return {"Error": "Amigo a eliminar no especificador"}, 400
	return DbremoveFriend(username,friend)

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	return user