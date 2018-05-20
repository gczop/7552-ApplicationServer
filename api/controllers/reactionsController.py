import json
from flask import request
from api.utils import *
from SharedServerRequests.userLogin import *
from databases.stories import storiesDb
from databases.loginedUsers import loginedUsers

def getStoryReactions(request):
	storyID = getRequestHeader(request,"story-id") 
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 26)"}, 400
	return storiesDb.getStoryReactions(storyID)

def addNewReaction(request):
	storyID = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	#TODO corregir esto plox
	reaction = getRequestHeader(request,"reaction")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 27)"}, 400
	if (username == None):
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 28)"}, 400
	if (reaction == None):
		return {"Error": "Falta de informacion en header. Reaccion no especificada (Error code: 29)"}, 400
	return storiesDb.addStoryReaction(storyID,username,reaction)
		

def removeReaction(request):
	storyID = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 30)"}, 400
	if (username == None):
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 31)"}, 400
	return storiesDb.deleteStoryReaction(storyID,username)

