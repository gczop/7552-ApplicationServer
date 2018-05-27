import requests
import os
from logger.log import *

MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    log("Shared Server found in Mongo")
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    log("Shared Server found in Travis")
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    log("Shared Server found in localhost")
    #sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
    sharedServerDir = "http://localhost:10010"
    #sharedServerDir = "http://web-shared:10010" #DOCKER-TAG

def authenticateUserLogin(username,password):
    log("Shared server request: login user")
    payload = {
  		"username": username,
  		"password": password
    }
    print(payload)
    print (sharedServerDir + '/api/token')
    return requests.post(sharedServerDir + '/api/token', data= payload)
