import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.flashStories import flashStoriesDb
# from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers

numberOfStoriesToSee = 10

def getHomepageFeed(request):
	username = getRequestHeader(request,"username")
	logDebug("flashStoriesController- getting "+str(username)+" homepage feed")
	if(username == None):
		logErrorCode("API46",username)
		return {"Error": "Falta de informacion en header username no especificado (Error code: 46)"}, 400
	return { "feedStories" : flashStoriesDb.getUserLastNStories(username,numberOfStoriesToSee)}, 200

def addNewStory(request):
	username = getRequestHeader(request,"username")
	storyInfo = getRequestData(request)
	logDebug("flashStoriesController- "+str(username)+" adding new flash story")
	if(username == None):
		logErrorCode("API47")
		return {"Error": "Falta de informacion en header username no especificado (Error code: 47)"}, 400
	id = flashStoriesDb.addNewStory(username,storyInfo)
	# commentsDb.addComments(id)
	return { 'storyId' : id}, 200

def updateStory(request):
    username = getRequestHeader(request,"username")
    id = getID(request)
    storyInfo = getRequestData(request)
    logDebug("flashStoriesController- "+str(username)+" updating flash story"+str(id))
    if(id == None):
        logErrorCode("API48")
        return {"Error": "Falta de informacion en header username no especificado (Error code: 48)"}, 400
    if(storyInfo["url"] !=None):
        logErrorCode("API49", str(storyInfo["url"]))
        return {"Error": "No se puede modificar informacion vital del archivo mutlimedia (Error code: 49)"}, 401
    flashStoriesDb.updateStory(username, id,storyInfo)
    return { 'storyId' : id }, 200

def removeStory(request):
	# username = getUserName(request)
	id = getRequestHeader(request,"id")
	logDebug("flashStoriesController- removing story "+str(id))
	if(id == None):
		logErrorCode("API50")
		return {"Error": "Falta de informacion en header username no especificado (Error code: 50)"}, 400
	return { 'state': flashStoriesDb.deleteStory(id)},200


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
