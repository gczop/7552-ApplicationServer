import json
from flask import request
from SharedServerRequests.userLogin import *
from databases.users import usersDb
from databases.loginedUsers import loginedUsers

def getUserProfile(request):
    data = json.loads(request.data); username = data.get("username")
    if(username == None):
        return {"Error": "Usuario no especificado en el header (Error code: 19)"}, 400
    return usersDb.getUserProfile(username)

def updateUserProfile(request):
    data = json.loads(request.data);
    username = data.get("username")
    if(username == None):
        return {"Error": "Usuario no especificado en el header (Error code: 20)"}, 400
    personalInfo = data.get("personalInformation")
    return usersDb.updateUserProfile(username,personalInfo)
