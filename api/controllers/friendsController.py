import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.friends import friendsDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getUserFriends(request):
	username = getRequestHeader(request,'username')
	print(username)
	log("Getting "+str(username)+" friend list")
	if(username == None):
		logError("API13")
		return {"Error": "Falta de informacion en header (Error code: 13)"}, 400
	return friendsDb.getUserFriends(username)

#For testing purposes
def addFriend(request):
	username = getRequestHeader(request,"username")
	friend = getRequestHeader(request,"friend")
	log("Adding "+str(friend)+" to "+str(username)+" friend list")
	if(username == None or friend == None):
		logError("API14")
		return {"Error": "Falta de informacion en header (Error code: 14)"}, 400
	try:
		return friendsDb.addNewFriend(username,friend)
	except:
		logError("API26")
		return {"Error": "No se pudo agregar esta persona a tu lista de amigos (Error code: 26?)"}, 401


def removeFriend(request):
    username = getRequestHeader(request,"username")
    friend = getRequestHeader(request,"friend")
    log("Removing "+str(friend)+" from "+str(username)+" friend list")
    if(username == None):
        logError("API14b")
        return {"Error": "Falta de informacion en header (Error code: 14b)"}, 400
    if(friend == None):
        logError("API15")
        return {"Error": "Amigo a eliminar no especificado (Error code: 15)"}, 400
    try:
        return friendsDb.removeFriend(username,friend)
    except:
        logError("API25")
        return {"Error": "Esta persona no esta en tu lista de amigos (Error code: 25)"}, 401


def getSpecificUserFriends(username):
    log("Getting "+str(username)+" friend list")
    if(username == None):
        logError("API16")
        return {"Error": "Usuario no especificado (Error code: 16)"}, 400
    userFriends = friendsDb.getUserFriends(username)
    if(userFriends == None):
        logError("API17")
        return {"Error": "Usuario no registrado o aun sin amigos agregados (Error code: 17)"}, 400
    return userFriends
