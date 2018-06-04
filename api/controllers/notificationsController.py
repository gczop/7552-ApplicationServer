import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.notifications import notificationsDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getUserNotifications(request):
	username = getRequestHeader(request,"username")
	logDebug("notificationsController- Getting notifications for user "+str(username))
	if(username == None):
		logErrorCode("API18")
		return {"Error": "Falta de informacion en header (Error code: 18)"}, 400
	return notificationsDb.getUserNotifications(username)

