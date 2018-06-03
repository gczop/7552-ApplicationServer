import requests
from requests.auth import HTTPBasicAuth as ReqAuth
from databases.auth import authenticationsDb
from SharedServerRequests.serverAuthentication import serverAuthenticator
import os
from logger.log import *

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("userLogin: Shared Server found in Mongo")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    logInfo("userLogin: Shared Server found in Travis")
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("userLogin: Shared Server found in localhost")
    #sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    sharedServerDir = "http://localhost:10010"
    #sharedServerDir = "http://web-shared:10010" #DOCKER-TAG

def authenticateUserLogin(username,password):
    logInfo("userLogin- Shared server request: authenticate login user")
    payload = {
  		"username": username,
  		"password": password
    }
    logDebug("userLogin- "+str(payload)+" "+str(serverAuthenticator.serverUser))
    user,s_password = authenticationsDb.getAuthentication()
    return requests.post(sharedServerDir + '/api/token',  
        auth=ReqAuth(user,s_password), data= payload)
