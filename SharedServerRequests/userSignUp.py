import requests
import os
from logger.log import *

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    log("UserSignup: Shared Server found in Mongo")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    log("UserSignup: Shared Server found in Travis")
    # Not on an app with the MongoHQ add-on, do some localhost action
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com" #"http://localhost:10010"
else:
	#sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    log("UserSignup: Shared Server found in localhost")
    sharedServerDir = "http://localhost:10010"
    #sharedServerDir = "http://web-shared:10010" #DOCKER-TAG
    print (sharedServerDir)

def registerNewUser(username,password,fbToken):
	log("Shared Server request: user signup")
	payload = {
 	 "username": username,
 	 "password": password,
 	 "facebookAuthToken": fbToken
	}
	print (payload)
	return requests.post(sharedServerDir +  '/api/authorize', data= payload)
