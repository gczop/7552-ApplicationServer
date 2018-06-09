import os
import pymongo
from pymongo import MongoClient
from logger.log import *

import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    conn = pymongo.MongoClient(MONGO_URL)
    logInfo("invitations- Invitations DB in MONGO")
    from urllib.parse import urlparse
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("invitations- Invitations DB in localhost")
    conn = pymongo.MongoClient('localhost', 27017)
    #conn = pymongo.MongoClient('mongo', 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']


invitationsCollection = db.Invitations

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class InvitationsDb(Singleton):
    invitationsList = invitationsCollection

    def getUserInvitations(self,username):
        logDebug("invitations- Getting user "+str(username)+ " invitations")
        return self.invitationsList.find_one({"username":username})["invitations"]

    def addFriendInvitation(self,username,friend):
        logDebug("invitations- Adding friend invitation")
        try:
            invitations = self.invitationsList.find_one({"username":friend})["invitations"]
            if(username in invitations):
                return 'Okey'
            invitations.append(username)
            print("\n\nuserINVITATIONS",invitations);
            self.invitationsList.find_one_and_update({"username":friend},
                                                     {"$set": {"invitations": invitations}},upsert=True)
            return "Okey"
        except:
            self.invitationsList.insert_one({"username":friend, "invitations":[username]})
            return "Okey"

    def acceptFriendInvitation(self,username,friend):
        logDebug("invitations- Accepting friend invitation: "+str(username)+"|"+str(friend))
        userInvitations = self.invitationsList.find_one({"username":username})["invitations"]
        # NO SE PORQUE SE BORRA EN OTRO LADO
        userInvitations.remove(friend)
        self.invitationsList.find_one_and_update({"username":username},
                                                 {"$set": {"friends": userInvitations}},upsert=True)
        return "Okey"

invitationsDb = InvitationsDb()

# def DbgetUserInvitations(username):
#     return invitationsCollection.find_one({"username":username})["invitations"]

# def DbaddFriendInvitation(username,friend):
#     try:
#         userInvitations = invitationsCollection.find_one({"username":friend})["invitations"]
#         userInvitations.append(username)
#         invitationsCollection.find_one_and_update({"username":friend},
#             {"$set": {"friends": userInvitations}},upsert=True)
#         return "Okey"
#     except:
#         invitationsCollection.insert_one({"username":friend, "invitations":[username]})
#         return "Okey"

# def DbacceptFriendInvitation(username,friend):
#     userInvitations = invitationsCollection.find_one({"username":username})["invitations"]
#     userInvitations.remove(friend)
#     invitationsCollection.find_one_and_update({"username":username},
#         {"$set": {"invitations": userInvitations}},upsert=True)
#     return "Okey"

# def authenticateUser(token= None):
# 	print("LLegamos a auth" + token)
# 	if(token != None):
# 		return friendsCollection.find_one({"app_token":token})
# 	return None


