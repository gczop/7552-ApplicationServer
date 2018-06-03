import os
import pymongo
from pymongo import MongoClient
from pymongo import ReturnDocument
from logger.log import *
import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    logInfo("friends- Friends DB in MONGO")
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("friends- Friends DB in localhost")
    #conn = pymongo.MongoClient('localhost', 27017)
    conn = pymongo.MongoClient('mongo', 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']


friendsCollection = db.Friends


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class FriendsDb(Singleton):
    friendsList = friendsCollection

    def getUserFriends(self,username):
        logDebug("friends- Getting "+str(username)+" friend list")
        try:
            return self.friendsList.find_one({"username":username})["friends"]
        except:
            return self.friendsList.find_one_and_update({"username":username},
            {"$set": {"friends": []}},upsert=True,return_document=ReturnDocument.AFTER)["friends"]

    def removeFriend(self,username,friend):
        logDebug("friends- "+str(username)+" deleting "+str(friend)+ " from friends list")
        userFriends = self.friendsList.find_one({"username":username})["friends"]
        userFriends.remove(friend)
        self.friendsList.find_one_and_update({"username":username},
            {"$set": {"friends": userFriends}},upsert=True)
        userFriends = self.friendsList.find_one({"username":friend})["friends"]
        userFriends.remove(username)
        self.friendsList.find_one_and_update({"username":friend},
            {"$set": {"friends": userFriends}},upsert=True)
        return "Okey"

    def addNewFriend(self,username,newFriend):
        logDebug("friends- "+str(username)+" adding "+str(newFriend)+ " to friends list")
        try:
            userFriends = self.friendsList.find_one({"username":username})["friends"]
            if newFriend not in userFriends:
                userFriends.append(newFriend)
            self.friendsList.find_one_and_update({"username":username},
                {"$set": {"friends": userFriends}},upsert=True)
        except:
            self.friendsList.insert_one({"username":username, "friends":[newFriend]})
        logDebug("friends- "+str(newFriend)+" adding "+str(username)+ " to friends list")
        try:
            userFriends = self.friendsList.find_one({"username":newFriend})["friends"]
            if username not in userFriends:
                userFriends.append(username)
            self.friendsList.find_one_and_update({"username":newFriend},
                {"$set": {"friends": userFriends}},upsert=True)
        except:
            self.friendsList.insert_one({"username":newFriend, "friends":[username]})

friendsDb = FriendsDb()


# def DbgetUserFriends(username):
#     return friendsCollection.find_one({"username":username})["friends"]

# def DbremoveFriend(username,friend):
#     userFriends = friendsCollection.find_one({"username":username})["friends"]
#     userFriends.remove(friend)
#     friendsCollection.find_one_and_update({"username":username},
#         {"$set": {"friends": userFriends}},upsert=True)
#     userFriends = friendsCollection.find_one({"username":friend})["friends"]
#     userFriends.remove(username)
#     friendsCollection.find_one_and_update({"username":friend},
#         {"$set": {"friends": userFriends}},upsert=True)
#     return "Okey"

# def DbaddNewFriend(username,newFriend):
#     try:
#         userFriends = friendsCollection.find_one({"username":username})["friends"]
#         userFriends.append(newFriend)
#         friendsCollection.find_one_and_update({"username":username},
#             {"$set": {"friends": userFriends}},upsert=True)
#     except:
#         friendsCollection.insert_one({"username":username, "friends":[newFriend]})
#     try:
#         userFriends = friendsCollection.find_one({"username":newFriend})["friends"]
#         userFriends.append(username)
#         friendsCollection.find_one_and_update({"username":newFriend},
#             {"$set": {"friends": userFriends}},upsert=True)
#     except:
#         friendsCollection.insert_one({"username":newFriend, "friends":[username]})
# def authenticateUser(token= None):
# 	print("LLegamos a auth" + token)
# 	if(token != None):
# 		return friendsCollection.find_one({"app_token":token})
# 	return None


