import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.friends import friendsDb
from databases.invitations import invitationsDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getUserInvitations(request):
	username = getRequestHeader(request,"username")
	friend = getRequestHeader(request,"friend")
	log("Retrieving invitations for user "+str(username))
	if(username == None):
		logError("API06")
		return {"Error": "Falta de informacion en header (Error code: 6)"}, 400
	try:
		return invitationsDb.getUserInvitations(username)
	except:
		logError("API07", username)
		return {"Error": "Aun no tiene invitaciones (Error code: 7)"}

def addFriendInvitation(request):
	username = getRequestHeader(request,"username")
	newFriend = getRequestHeader(request,"friend")
	log(str(username)+" adding "+str(newFriend)+" to friend list")
	if(username == None):
		logError("API08")
		return {"Error": "Falta de informacion en header (Error code: 8)"}, 400
	if(newFriend == None):
		logError("API09")
		return {"Error": "Amigo a agregar no especificado (Error code: 9)"}, 400
	return invitationsDb.addFriendInvitation(username,newFriend)

def acceptFriendInvitation(request):
	username = getRequestHeader(request,"username")
	newFriend = getRequestHeader(request,"friend")
	log(str(username)+" accepting "+str(newFriend)+" friend request")
	if(username == None):
		logError("API10")
		return {"Error": "Falta de informacion en header (Error code: 10)"}, 400
	if(newFriend == None):
		logError("API11")
		return {"Error": "Amigo a aceptar no especificado (Error code: 11)"}, 400
	print(username,newFriend)
	try:
		invitationsDb.acceptFriendInvitation(username,newFriend)
	except:
		logError("API12", username, newFriend)
		return {"Error": "Invitacion a aceptar no es correcta (Error code: 12)"}, 401
	friendsDb.addNewFriend(username,newFriend)
	return "Okey"

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	friend = data.get("friend")
	return user, friend
