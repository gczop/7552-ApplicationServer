import json
from flask import request
from SharedServerRequests.serverAuthentication import serverAuthenticator
from api.utils import *

def authenticateServer(request):
    serverId = getRequestData(request)
    if(serverId == None):
        return {"Error": "Server ID no especificado"}, 400
    try:
        return serverAuthenticator.authenticateServer(serverId)
    except NameError:
        return {'Error': "Incorrect Server Id" }, 404


def getRequestData(request):
    print("AUTH")
    print(request.data)
    data = json.loads(request.data)
    serverId = data.get("serverId")
    return serverId