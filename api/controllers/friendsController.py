import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.friends import friendsDb
from databases.loginedUsers import loginedUsers

def getUserFriends(request):
	username = request.headers.get("username")
	print("AAaaaaa" + username)
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 13)"}, 400
	return friendsDb.getUserFriends(username)

def removeFriend(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 14)"}, 400
	friend = getRequestData(request)
	if(friend == None):
		return {"Error": "Amigo a eliminar no especificado (Error code: 15)"}, 400
	return friendsDb.removeFriend(username,friend)

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	return user

def getSpecificUserFriends(username):
	if(username == None):
		return {"Error": "Usuario no especificado (Error code: 16)"}, 400
	userFriends = friendsDb.getUserFriends(username)
	if(userFriends == None):
		return {"Error": "Usuario no registrado o aun sin amigos agregados (Error code: 17)"}, 400
	return userFriends