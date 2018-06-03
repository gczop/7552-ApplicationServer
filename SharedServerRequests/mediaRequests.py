import requests
import os
import json

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("mediaRequests- SharedServer found in MONGO")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
else:
    logInfo("mediaRequests- SharedServer found in localhost")
    #sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    #sharedServerDir = "http://localhost:10010"
    sharedServerDir = "http://web-shared:10010" #DOCKER-TAG
    print (sharedServerDir)



class ServerAuthentication(object):
	serverUser = None
	serverPassword = None
	def authenticateServer(self, serverId):
		logInfo("mediaRequests- Beggining server authentication")
		logDebug("mediaRequests- -Authenticating server:"+str(serverId))
		response = requests.post(sharedServerDir + '/api/servers/' + serverId)
		logDebug("mediaRequests- Response: "+str(response.text))
		if(response.status_code != 200):
			logErrorCode("AUTHSERVER01")
			raise NameError('Incorrect Server Auhtentication')
		responseData = json.loads(response.text)
		self.serverUser = serverId
		self.serverPassword = responseData['token']
		logInfo("mediaRequests- Authentication succesful")
		return {"Message": "Autenticacion Exitosa"} , 200

serverAuthenticator = ServerAuthentication()
