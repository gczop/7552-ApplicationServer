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


def DbgetUserFriends(username):
    print("AAAAAAACA")
    return friendsCollection.find_one({"username":username})["friends"]

def DbremoveFriend(username,friend):
    userFriends = friendsCollection.find_one({"username":username})["friends"]
    userFriends.remove(friend)
    friendsCollection.find_one_and_update({"username":username},
        {"$set": {"friends": userFriends}},upsert=True)
    return "Okey"

def DbaddNewFriend(username,newFriend):
    try:
        print("Pasamos por el try")
        userFriends = friendsCollection.find_one({"username":username})["friends"]
        print("Pasamos por el try")
        userFriends.append(newFriend)
        friendsCollection.find_one_and_update({"username":username},
            {"$set": {"friends": userFriends}},upsert=True)
    except:
        print("Vamos al except")
        friendsCollection.insert_one({"username":username, "friends":[newFriend]})
        print("Funco")
    try:
        userFriends = friendsCollection.find_one({"username":newFriend})["friends"]
        userFriends.append(username)
        friendsCollection.find_one_and_update({"username":newFriend},
            {"$set": {"friends": userFriends}},upsert=True)
    except:
        print("Vamos al except")
        friendsCollection.insert_one({"username":newFriend, "friends":[username]})
        print("Funco")
# def authenticateUser(token= None):
# 	print("LLegamos a auth" + token)
# 	if(token != None):
# 		return friendsCollection.find_one({"app_token":token})
# 	return None


