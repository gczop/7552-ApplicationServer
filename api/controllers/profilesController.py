import json
from flask import request
from SharedServerRequests.userLogin import *
from api.utils import *
from databases.users import usersDb
from databases.loginedUsers import loginedUsers
from logger.log import *

def getUserProfile(request):
    username = getRequestHeader(request,"username")
    logDebug("profilesController- Getting "+str(username)+" profile")
    if(username == None):
        logErrorCode("API19")
        return {"Error": "Usuario no especificado en el header (Error code: 19)"}, 400
    return usersDb.getUserProfile(username)

def updateUserProfile(request):
    data = json.loads(request.data);
    username = getRequestHeader(request,"username")
    logDebug("profilesController- Updating "+str(username)+" profile")
    if(username == None):
        logErrorCode("API20")
        return {"Error": "Usuario no especificado en el header (Error code: 20)"}, 400
    personalInfo = data.get("personalInformation")
    return usersDb.updateUserProfile(username,personalInfo)
