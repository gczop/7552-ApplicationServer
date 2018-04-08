import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.conversations import conversationsDb

def getUserConversations(request):
	username = request.headers.get("username")
	if (username == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 38)"},400
	return conversationsDb.getUserConversations(username)


def createNewConversation(request):
	firstUser = request.headers.get("first-username")
	secondUser = request.headers.get("second-username")
	if (firstUser == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 39)"},400
	if (secondUser == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 40)"},400	
	return conversationsDb.createConversation(firstUser, secondUser)
