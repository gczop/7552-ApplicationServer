import requests
import os


MONGO_URL = os.environ.get('MONGODB_URI')
TRAVIS_URL = os.environ.get('TRAVIS_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
elif TRAVIS_URL:
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    sharedServerDir = "https://blooming-lowlands-52198.herokuapp.com"
 	#sharedServerDir = "http://localhost:10010"

def authenticateUserLogin(username,password):
    payload = {
  		"username": username,
  		"password": password
    }
    print(payload)
    # print (sharedServerDir + '/api/token')
    return requests.post(sharedServerDir + '/api/token', data= payload)