import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.flashStories import flashStoriesDb
# from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers

if 'TEST_ENV' in os.environ:
	from mockups.requests.mediaRequestsMockUp import *
else:
	from SharedServerRequests.mediaRequests import *

numberOfStoriesToSee = 10

def getHomepageFeed(request):
	username = getRequestHeader(request,"username")
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 21)"}, 400
	flashStoriesList = flashStoriesDb.getUserLastNStories(username,numberOfStoriesToSee)
	for story in flashStoriesList:
		response = getFirebaseUrl(story['storyDetail']['url'])
		if(response.status_code != 200):
			return {"Error": "Error inesperado obteniendo la url de una flash story" + story["storyDetail"]["url"]} , 400
		responseData = json.loads(response.text)
		story['storyDetail']['url']= responseData['resource']
	return { "feedStories" : flashStoriesList}, 200

def addNewStory(request):
	username = getRequestHeader(request,"username")
	storyInfo = getRequestData(request)
	if(username == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 22)"}, 400
	response = uploadNewFile(username,storyInfo['url'])
	if(response.status_code != 200):
		return{"Error": "Error inesperado en el upload de una flash story"}, 400
	responseData = json.loads(response.text)
	storyInfo["url"] = responseData["_rev"]
	id = flashStoriesDb.addNewStory(username,storyInfo)
	# commentsDb.addComments(id)
	return { 'storyId' : id}, 200

def updateStory(request):
    username = getRequestHeader(request,"username")
    id = getID(request)
    storyInfo = getRequestData(request)
    if(id == None):
        return {"Error": "Falta de informacion en header username no especificado (Error code: 23)"}, 400
    if(storyInfo["url"] !=None):
        return {"Error": "No se puede modificar informacion vital del archivo mutlimedia (Error code: 25)"}, 401
    flashStoriesDb.updateStory(username, id,storyInfo)
    return { 'storyId' : id }, 200

def removeStory(request):
	# username = getUserName(request)
	id = getRequestHeader(request,"id")
	if(id == None):
		return {"Error": "Falta de informacion en header username no especificado (Error code: 24)"}, 400
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
