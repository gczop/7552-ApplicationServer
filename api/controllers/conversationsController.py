import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
#from databases.conversations import conversationsDb
from logger.log import *

conversationsDb = 0
def getUserConversations(request):
	username = getRequestHeader(request,"username")
	log("Getting user "+str(username)+" conversations")
	if (username == None):
		logError("API38")
		return {"Error": "Falta de informacion en header. Usuario no especificado (Error code: 38)"},400
	return conversationsDb.getUserConversations(username)


def createNewConversation(request):
	firstUser = getRequestHeader(request,"first-username") 
	secondUser =  getRequestHeader(request,"second-username")
	log("Creating conversation between "+str(firstUser)+"-"+str(secondUser))
	if (firstUser == None):
		logError("API39")
		return {"Error": "Falta de informacion en header. Usuario no especificado (Error code: 39)"},400
	if (secondUser == None):
		logError("API40")
		return {"Error": "Falta de informacion en header. Usuario no especificado (Error code: 40)"},400	
	return conversationsDb.createConversation(firstUser, secondUser)
