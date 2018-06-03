import requests
from requests.auth import HTTPBasicAuth as ReqAuth
from SharedServerRequests.serverAuthentication import serverAuthenticator
import os
import datetime




MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("mediaRequests- SharedServer found in MONGO")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
else:
    logInfo("mediaRequests- SharedServer found in localhost")
    #sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    sharedServerDir = "http://localhost:10010"
    #sharedServerDir = "http://web-shared:10010" #DOCKER-TAG


def uploadNewFile(username,fileUrl):
    logInfo("mediaRequests- Uploading new file")
    logDebug("mediaRequests- "+str(username)+"||"+str(fileUrl))
    payload = {
  		"id": username,
  		"createdTime": str(datetime.datetime.now()),
  		"size": "anySize",
  		"filename": "noName",
  		"resource": fileUrl
    }
    print (sharedServerDir + '/api/files')
    return requests.post(sharedServerDir + '/api/files',  
        auth=ReqAuth(serverAuthenticator.serverUser,serverAuthenticator.serverPassword), data= payload)

def getFirebaseUrl(url):
	return requests.get(sharedServerDir + '/api/files/' + url)
