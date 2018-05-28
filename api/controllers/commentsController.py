import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getStoryComments(request):
	storyId = getRequestHeader(request,"story-id")
	log("Getting story comments from story "+str(storyId))
	if (storyId == None):
		logError("API32")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 32)"}, 400
	return { "comments" : commentsDb.getStoryComments(storyId) } , 200

def addNewComment(request):
	storyID = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	comment = getRequestData(request)
	log("Adding new comment from "+str(username)+" to story "+str(storyId))
	if (storyID == None):
		logError("API33")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 33)"}, 400
	if (username == None):
		logError("API34")
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 34)"}, 400
	if (comment == None):
		logError("API35")
		return {"Error": "Falta de informacion en header. Comentario no especificado (Error code: 35)"}, 400	
	return { "id": commentsDb.addNewComment(storyID, username, comment) } , 200

def removeComment(request):
	storyID = request.headers.get("story-id")
	commentID = request.headers.get("comment-id")
	log("Removing comment "+str(commentID)+" from story "+str(storyID))
	if (storyID == None):
		logError("API36")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 36)"}, 400
	if (commentID == None):
		logError("API37")
		return {"Error": "Falta de informacion en header. Comment ID no especificado (Error code: 37)"}, 400	
	return { "state": commentsDb.removeComment(storyID, commentID) } , 200

def getRequestData(request):
	commentInfo = {}
	data = json.loads(request.data)
	commentInfo = data.get("comment")
	return commentInfo
