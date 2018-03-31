import os
import pymongo
from pymongo import MongoClient

import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    print("Conectamos local")
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['StoriesAppServer']


friendsCollection = db.Friends


def getUserFriends(username):
    return friendsCollection.find_one({"username":username})

def removeFriend(username,friend):
    userFriends = friendsCollection.find_one({"username":username})["friends"]
    userToRemoveIndex = userFriends.index(friend)
    userFriends.remove(userToRemoveIndex)
    friendsCollection.find_one_and_update({"username":username},
        {"$set": {"friends": userFriends}},upsert=True)
# def authenticateUser(token= None):
# 	print("LLegamos a auth" + token)
# 	if(token != None):
# 		return friendsCollection.find_one({"app_token":token})
# 	return None


