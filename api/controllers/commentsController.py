import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.comments import commentsDb
from databases.loginedUsers import loginedUsers

def getStoryComments(request):
	storyId = request.headers.get("story-id")
	if (storyId == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 32)"}, 400
	return commentsDb.getStoryComments(storyId)	

def addNewComment(request):
	storyID = request.headers.get("story-id")
	username = request.headers.get("username")
	comment = request.headers.get("comment")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 33)"}, 400
	if (username == None):
		return {"Error": "Falta de informacion en header. Username no especificado (Error code: 34)"}, 400
	if (comment == None):
		return {"Error": "Falta de informacion en header. Comentario no especificado (Error code: 35)"}, 400	
	return commentsDb.addNewComment(storyID, username, comment)

def removeComment(request):
	storyID = request.headers.get("story-id")
	commentID = request.headers.get("comment-id")
	if (storyID == None):
		return {"Error": "Falta de informacion en header. Story id no especificado (Error code: 36)"}, 400
	if (commentID == None):
		return {"Error": "Falta de informacion en header. Comment ID no especificado (Error code: 37)"}, 400	
	return commentsDb.removeComment(storyID, commentID)
