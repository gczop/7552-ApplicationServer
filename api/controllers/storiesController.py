import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.stories import storiesDb
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers

numberOfStoriesToSee = 3

def getHomepageFeed(request):
	username = getUserName(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 21)"}, 400
	return storiesDb.getUserLastNStories(username,numberOfStoriesToSee)

def addNewStory(request):
	username = getUserName(request)
	storyInfo = getRequestData(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 22)"}, 400
	id = storiesDb.addNewStory(username,storyInfo)
	commentsDb.addComments(id)
	return id

def updateStory(request):
	username = getUserName(request)
	storyInfo = getRequestData(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 23)"}, 400
	if(storyInfo["url"] !=None or storyInfo["owner"] != None or storyInfo["storyId"] != None):
		return {"Error": "No se puede modificar informacion vital del archivo mutlimedia (Error code: 25)"}, 401
	return storiesDb.updateStory(username,storyInfo)

def removeStory(request):
	# username = getUserName(request)
	id = getID(request)
	if(id == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 24)"}, 400
	return storiesDb.deleteStory(id)

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
	storyInfo["state"] = data.get("state")
	storyInfo["description"] = data.get("description")
	return storyInfo
