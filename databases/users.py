import os
import pymongo
from pymongo import MongoClient

import pymongo

MONGO_URL = os.environ.get('MONGOHQ_URL')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    conn = pymongo.MongoClient(MONGO_URL)
    
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    print("Conectamos local")
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['StoriesAppServer']


userCollection = db.User




def authenticate_user(token= None, email= None, password= None):
	print("LLegamos a auth" + token + email + password)
	if(token != None):
		return userCollection.find_one({"app_token":token})
	return None


