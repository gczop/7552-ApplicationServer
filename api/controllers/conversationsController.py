import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
#from databases.conversations import conversationsDb

conversationsDb = 0
def getUserConversations(request):
	username = getRequestHeader(request,"username")
	if (username == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 38)"},400
	return conversationsDb.getUserConversations(username)


def createNewConversation(request):
	firstUser = getRequestHeader(request,"first-username") 
	secondUser =  getRequestHeader(request,"second-username")
	if (firstUser == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 39)"},400
	if (secondUser == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 40)"},400	
	return conversationsDb.createConversation(firstUser, secondUser)
