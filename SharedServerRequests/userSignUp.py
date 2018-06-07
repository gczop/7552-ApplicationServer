import requests
import os
from logger.log import *
from requests.auth import HTTPBasicAuth as ReqAuth
from databases.auth import authenticationsDb
from SharedServerRequests.serverAuthentication import serverAuthenticator

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("UserSignup- Shared Server found in Mongo")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    logInfo("UserSignup- Shared Server found in Travis")
    # Not on an app with the MongoHQ add-on, do some localhost action
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com" #"http://localhost:10010"
else:
	#sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    logInfo("UserSignup- Shared Server found in localhost")
    sharedServerDir = "http://localhost:10010"
    #sharedServerDir = "http://web-shared:10010" #DOCKER-TAG
    print (sharedServerDir)


def registerNewUser(username,password,fbToken):
	logInfo("UserSignup- Shared Server request: registering new user")
	payload = {
 	 "username": username,
 	 "password": password,
 	 "facebookAuthToken": fbToken
	}
	logDebug("UserSignup- "+str(payload)+" "+str(serverAuthenticator.serverUser))
	print (payload, serverAuthenticator.serverUser, serverAuthenticator.serverPassword)
	user,s_password = authenticationsDb.getAuthentication()
	return requests.post(sharedServerDir +  '/api/authorize',
        auth=ReqAuth(user,s_password), data= payload)
