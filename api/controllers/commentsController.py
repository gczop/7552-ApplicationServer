import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers

def getStoryComments(request):
	storyId = getRequestHeader(request,"story-id")
	if (storyId == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 32)"}, 400
	return { "comments" : commentsDb.getStoryComments(storyId) } , 200

def addNewComment(request):
	storyID = getRequestHeader(request,"story-id")
	username = getRequestHeader(request,"username")
	comment = getRequestData(request)
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 33)"}, 400
	if (username == None):
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 34)"}, 400
	if (comment == None):
		return {"Error": "Falta de informacion en header. Comentario no especificado (Error code: 35)"}, 400	
	return { "id": commentsDb.addNewComment(storyID, username, comment) } , 200

def removeComment(request):
	storyID = request.headers.get("story-id")
	commentID = request.headers.get("comment-id")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 36)"}, 400
	if (commentID == None):
		return {"Error": "Falta de informacion en header. Comment ID no especificado (Error code: 37)"}, 400	
	return { "state": commentsDb.removeComment(storyID, commentID) } , 200

def getRequestData(request):
	commentInfo = {}
	data = json.loads(request.data)
	commentInfo = data.get("comment")
	return commentInfo
