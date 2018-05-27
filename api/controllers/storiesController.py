import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.stories import storiesDb
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers
from logger.log import *

numberOfStoriesToSee = 3

def getHomepageFeed(request):
	username = getRequestHeader(request,"username")
	log("Retrieving homepage feed for "+str(username))
	if(username == None):
		logError("API21")
		return {"Error": "Falta de informacion en header username no especificado (Error code: 21)"}, 400
	return { "feedStories" : storiesDb.getUserLastNStories(username,numberOfStoriesToSee)}, 200

def addNewStory(request):
	username = getRequestHeader(request,"username")
	storyInfo = getRequestData(request)
	log("Adding story for user "+str(username))
	if(username == None):
		logError("API22")
		return {"Error": "Falta de informacion en header username no especificado (Error code: 22)"}, 400
	id = storiesDb.addNewStory(username,storyInfo)
	commentsDb.addComments(id)
	return { 'storyId' : id}, 200

def updateStory(request):
    username = getRequestHeader(request,"username")
    id = getID(request)
    storyInfo = getRequestData(request)
    log("Updating story "+str(id))
    if(id == None):
        logError("API23")
        return {"Error": "Falta de informacion en header username no especificado (Error code: 23)"}, 400
    if(storyInfo["url"] !=None):
        logError("API43", storyInfo)
        return {"Error": "No se puede modificar informacion vital del archivo mutlimedia (Error code: 43)"}, 401
    storiesDb.updateStory(username, id,storyInfo)
    return { 'storyId' : id }, 200

def removeStory(request):
	# username = getUserName(request)
	id = getRequestHeader(request,"id")
	log("Deleting story "+str(id))
	if(id == None):
		logError("API24")
		return {"Error": "Falta de informacion en header username no especificado (Error code: 24)"}, 400
	return { 'state': storiesDb.deleteStory(id)},200


def getUserName(request):
    data = json.loads(request.data)
    return data.get("username")

def getID(request):
    data = json.loads(request.data)
    return data.get("id")

def getRequestData(request):
	storyInfo = {}
	data = json.loads(request.data)
	storyInfo["url"] = data.get("url")
	storyInfo["title"] = data.get("title")
	storyInfo["state"] = data.get("state")
	storyInfo["description"] = data.get("description")
	return storyInfo
