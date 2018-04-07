import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.stories import storiesDb
from databases.loginedUsers import loginedUsers

def getStoryReactions(request):
	storyID = request.headers.get("story-id")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 26)"}, 400
	return storiesDb.getStoryReactions(storyID)

def addNewReaction(request):
	storyID = request.headers.get("story-id")
	username = request.headers.get("username")
	reaction = request.headers.get("reaction")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 27)"}, 400
	if (username == None):
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 28)"}, 400
	if (reaction == None):
		return {"Error": "Falta de informacion en header. Reaccion no especificada (Error code: 29)"}, 400
	return storiesDb.addStoryReaction(storyID,username,reaction)
		

def removeReaction(request):
	storyID = request.headers.get("story-id")
	username = request.headers.get("username")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 30)"}, 400
	if (username == None):
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 31)"}, 400
	return storiesDb.removeReaction(storyID,username)	

