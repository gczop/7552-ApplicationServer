import requests
import os
from requests.auth import HTTPBasicAuth as ReqAuth
from SharedServerRequests.serverAuthentication import serverAuthenticator

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    # Not on an app with the MongoHQ add-on, do some localhost action
 	sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com" #"http://localhost:10010"
else:
	#sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    sharedServerDir = "http://localhost:10010"
    #sharedServerDir = "http://web-shared:10010" #DOCKER-TAG
    print (sharedServerDir)

def registerNewUser(username,password,fbToken):
	payload = {
 	 "username": username,
 	 "password": password,
 	 "facebookAuthToken": fbToken
	}
	print (payload, serverAuthenticator.serverUser, serverAuthenticator.serverPassword)
	return requests.post(sharedServerDir +  '/api/authorize',
        auth=ReqAuth(serverAuthenticator.serverUser,serverAuthenticator.serverPassword), data= payload)
