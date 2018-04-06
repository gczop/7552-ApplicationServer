import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.notifications import notificationsDb
from databases.loginedUsers import loginedUsers

def getUserNotifications(request):
	username = request.headers.get("username")
	if(username == None):
		return {"Error": "Falta de informacion en header (Error code: 18)"}, 400
	return notificationsDb.getUserNotifications(username)

