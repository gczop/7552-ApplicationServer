import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.friends import friendsDb
from databases.invitations import invitationsDb
from databases.loginedUsers import loginedUsers

def getUserInvitations(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 6)"}, 400
	try:
		return invitationsDb.getUserInvitations(username)
	except:
		return {"Error": "Aun no tiene invitaciones (Error code: 7)"}

def addFriendInvitation(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 8)"}, 400
	newFriend = getRequestData(request)
	if(newFriend == None):
		return {"Error": "Amigo a agregar no especificado (Error code: 9)"}, 400
	print(username,newFriend)
	return invitationsDb.addFriendInvitation(username,newFriend)

def acceptFriendInvitation(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 10)"}, 400
	newFriend = getRequestData(request)
	if(newFriend == None):
		return {"Error": "Amigo a aceptar no especificado (Error code: 11)"}, 400
	print(username,newFriend)
	try:
		invitationsDb.acceptFriendInvitation(username,newFriend)
	except:
		return {"Error": "Invitacion a aceptar no es correcta (Error code: 12)"}, 401
	friendsDb.addNewFriend(username,newFriend)
	return "Okey"

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	return user