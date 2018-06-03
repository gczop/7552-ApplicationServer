import requests
import os
import json
from logger.log import *

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("serverAuth-SharedServer found in MONGO")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
else:
	#sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    logInfo("serverAuth-SharedServer found in localhost")
    #sharedServerDir = "http://localhost:10010"
    sharedServerDir = "http://web-shared:10010" #DOCKER-TAG
    logInfo(sharedServerDir)



class ServerAuthentication(object):
	serverUser = None
	serverPassword = None
	def authenticateServer(self, serverId):
		logInfo("serverAuth-Beggining server authentication")
		logDebug("serverAuth-Authenticating server:"+str(serverId))
		response = requests.post(sharedServerDir + '/api/servers/' + serverId)
		logDebug("serverAuth-Response: "+str(response.text))
		if(response.status_code != 200):	
			logErrorCode("AUTHSERVER01")
			raise NameError('Incorrect Server Auhtentication')
		responseData = json.loads(response.text)
		self.serverUser = serverId
		self.serverPassword = responseData['token']
		logInfo("serverAuth-Authentication succesful")
		return {"Message": "Autenticacion Exitosa"} , 200

serverAuthenticator = ServerAuthentication()
