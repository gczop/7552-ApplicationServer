import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.friends import friendsDb
from databases.loginedUsers import loginedUsers

def getUserFriends(request):
	username = getRequestData(request)
	print(username)
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 13)"}, 400
	return friendsDb.getUserFriends(username)

#For testing purposes
def addFriend(request):
	data = json.loads(request.data)
	username = data.get("username")
	friend = data.get("friend")
	if(username == None or friend == None):
		return {"Error": "Falta de informacion en header (Error code: 14)"}, 400
	try:
		return friendsDb.addNewFriend(username,friend)
	except:
		return {"Error": "No se pudo agregar esta persona a tu lista de amigos (Error code: 26?)"}, 401


def removeFriend(request):
    data = json.loads(request.data)
    username = data.get("username")
    friend = data.get("friend")
    if(username == None):
        return {"Error": "Falta de informacion en header (Error code: 14)"}, 400
    if(friend == None):
        return {"Error": "Amigo a eliminar no especificado (Error code: 15)"}, 400
    try:
        return friendsDb.removeFriend(username,friend)
    except:
        return {"Error": "Esta persona no esta en tu lista de amigos (Error code: 25)"}, 401

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