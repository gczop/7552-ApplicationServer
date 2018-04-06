import requests
import os


MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    sharedServerDir = "https://morning-cove-52274.herokuapp.com"
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
 	sharedServerDir = "http://localhost:10010"

def authenticateUserLogin(username,password):
	payload = {
  		"username": username,
  		"password": password
	}
	return requests.post(sharedServerDir + '/api/token', data= payload)