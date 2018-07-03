import json
from flask import request
from api.utils import *
from SharedServerRequests.userLogin import *
from databases.stories import storiesDb
from databases.users import usersDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getStoryReactions(request):
	storyID = getRequestHeader(request,"story-id") 
	logDebug("reactionsController- Getting story "+str(storyID)+" reactions")
	if (storyID == None):
		logErrorCode("API42")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 42)"}, 400
	return { "reactions": storiesDb.getStoryReactions(storyID)}

def addNewReaction(request):
	storyID = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	#TODO corregir esto plox
	reaction = getRequestHeader(request,"reaction")
	logDebug("reactionsController- "+str(username)+" is adding a reaction to story "+str(storyID))
	if (storyID == None):
		logErrorCode("API27")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 27)"}, 400
	if (username == None):
		logErrorCode("API28")
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 28)"}, 400
	if (reaction == None):
		logErrorCode("API29")
		return {"Error": "Falta de informacion en header. Reaccion no especificada (Error code: 29)"}, 400
	usersDb.addNewUserInteraction(username,storyID)
	return { "reactions": storiesDb.addStoryReaction(storyID,username,reaction)}
		

def removeReaction(request):
	storyID = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	logDebug("reactionsController- "+str(username)+" is removing his reaction to story "+str(storyID))
	if (storyID == None):
		logErrorCode("API30")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 30)"}, 400
	if (username == None):
		logErrorCode("API31")
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 31)"}, 400
	return { "reactions": storiesDb.deleteStoryReaction(storyID,username)}

