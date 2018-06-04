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
	logDebug("invitationsController- Retrieving invitations for user "+str(username))
	if(username == None):
		logErrorCode("API06")
		return {"Error": "Falta de informacion en header (Error code: 6)"}, 400
	try:
		return invitationsDb.getUserInvitations(username)
	except:
		logErrorCode("API07", username)
		return {"Error": "Aun no tiene invitaciones (Error code: 7)"}

def addFriendInvitation(request):
	username = getRequestHeader(request,"username")
	newFriend = getRequestHeader(request,"friend")
	logDebug("invitationsController- "+str(username)+" adding "+str(newFriend)+" to friend list")
	if(username == None):
		logErrorCode("API08")
		return {"Error": "Falta de informacion en header (Error code: 8)"}, 400
	if(newFriend == None):
		logErrorCode("API09")
		return {"Error": "Amigo a agregar no especificado (Error code: 9)"}, 400
	return invitationsDb.addFriendInvitation(username,newFriend)

def acceptFriendInvitation(request):
	username = getRequestHeader(request,"username")
	newFriend = getRequestHeader(request,"friend")
	logDebug("invitationsController- "+str(username)+" accepting "+str(newFriend)+" friend request")
	if(username == None):
		logErrorCode("API10")
		return {"Error": "Falta de informacion en header (Error code: 10)"}, 400
	if(newFriend == None):
		logErrorCode("API11")
		return {"Error": "Amigo a aceptar no especificado (Error code: 11)"}, 400
	try:
		invitationsDb.acceptFriendInvitation(username,newFriend)
	except:
		logErrorCode("API12", username, newFriend)
		return {"Error": "Invitacion a aceptar no es correcta (Error code: 12)"}, 401
	friendsDb.addNewFriend(username,newFriend)
	return "Okey"

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	friend = data.get("friend")
	return user, friend
