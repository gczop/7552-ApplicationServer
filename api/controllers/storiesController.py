import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.stories import storiesDb
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers

numberOfStoriesToSee = 3

def getHomepageFeed(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 21)"}, 400
	return storiesDb.getUserLastNStories(username,numberOfStoriesToSee)

def addNewStory(username):
	username = request.headers.get("username")
	storyInfo = getRequestData(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 22)"}, 400
	newStory = storiesDb.addNewStory(username,storyInfo)
	commentsDb.addComments(newStory['_id'])
	return newStory

def updateStory(username):
	username = request.headers.get("username")
	storyInfo = getRequestData(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 23)"}, 400
	if(storyInfo["url"] !=None or storyInfo["owner"] != None or storyInfo["storyId"] != None):
		return {"Error": "No se puede modificar informacion vital del archivo mutlimedia (Error code: 25)"}, 401
	return storiesDb.updateStory(username,storyInfo)

def removeStory(username):
	username = request.headers.get("username")
	storyInfo = getRequestData(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 24)"}, 400
	return storiesDb.removeStory(username,storyInfo["storyId"])

def getRequestData(request):
	storyInfo = {}
	data = json.loads(request.data)
	storyInfo["storyId"] = data.get("storyId")
	storyInfo["url"] = data.get("url")
	storyInfo["owner"] = data.get("owner")
	storyInfo["state"] = data.get("state")
	storyInfo["description"] = data.get("description")
	return storyInfo
