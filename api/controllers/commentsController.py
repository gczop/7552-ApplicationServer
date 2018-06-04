import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getStoryComments(request):
	storyId = getRequestHeader(request,"story-id")
	logDebug("commentsController- Getting story comments from story "+str(storyId))
	if (storyId == None):
		logErrorCode("API32")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 32)"}, 400
	return { "comments" : commentsDb.getStoryComments(storyId) } , 200

def addNewComment(request):
	storyId = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	comment = getRequestData(request)
	logDebug("commentsController- Adding new comment from "+str(username)+" to story "+str(storyId))
	if (storyId == None):
		logErrorCode("API33")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 33)"}, 400
	if (username == None):
		logErrorCode("API34")
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 34)"}, 400
	if (comment == None):
		logErrorCode("API35")
		return {"Error": "Falta de informacion en header. Comentario no especificado (Error code: 35)"}, 400	
	return { "id": commentsDb.addNewComment(storyId, username, comment) } , 200

def removeComment(request):
	storyId = request.headers.get("story-id")
	commentID = request.headers.get("comment-id")
	logDebug("commentsController- Removing comment "+str(commentID)+" from story "+str(storyId))
	if (storyId == None):
		logErrorCode("API36")
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 36)"}, 400
	if (commentID == None):
		logErrorCode("API37")
		return {"Error": "Falta de informacion en header. Comment ID no especificado (Error code: 37)"}, 400	
	return { "state": commentsDb.removeComment(storyId, commentID) } , 200

def getRequestData(request):
	commentInfo = {}
	data = json.loads(request.data)
	commentInfo = data.get("comment")
	return commentInfo
