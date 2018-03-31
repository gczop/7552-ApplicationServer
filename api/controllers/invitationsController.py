import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.friends import *
from databases.invitations import *
from databases.loginedUsers import loginedUsers

def getUserInvitations(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header"}, 400
	try:
		return DbgetUserInvitations(username)
	except:
		return {"Error": "Aun no tiene invitaciones"}

def addFriendInvitation(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header"}, 400
	newFriend = getRequestData(request)
	if(newFriend == None):
		return {"Error": "Amigo a agregar no especificado"}, 400
	print(username,newFriend)
	return DbaddFriendInvitation(username,newFriend)

def acceptFriendInvitation(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header"}, 400
	newFriend = getRequestData(request)
	if(newFriend == None):
		return {"Error": "Amigo a aceptar no especificado"}, 400
	print(username,newFriend)
	try:
		DbacceptFriendInvitation(username,newFriend)
	except:
		return {"Error": "Invitacion a aceptar no es correcta"}, 401
	DbaddNewFriend(username,newFriend)
	return "Okey"

def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	return user