import json
from flask import request
from SharedServerRequests.serverAuthentication import serverAuthenticator
from api.utils import *
from logger.log import *

def authenticateServer(request):
    serverId = getRequestData(request)
    logDebug("statsController- authenticating server "+str(serverId))
    if(serverId == None):
        logErrorCode("API44", serverId)
        return {"Error": "Server ID no especificado"}, 400
    try:
        return serverAuthenticator.authenticateServer(serverId)
    except NameError:
        logErrorCode("API45")
        return {'Error': "Incorrect Server Id" }, 404


def getRequestData(request):
    data = json.loads(request.data)
    serverId = data.get("serverId")
    return serverId
