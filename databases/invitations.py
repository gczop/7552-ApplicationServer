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


invitationsCollection = db.Invitations


def DbgetUserInvitations(username):
    return invitationsCollection.find_one({"username":username})["invitations"]

def DbaddFriendInvitation(username,friend):
    try:
        userInvitations = invitationsCollection.find_one({"username":friend})["invitations"]
        userInvitations.append(username)
        invitationsCollection.find_one_and_update({"username":friend},
            {"$set": {"friends": userInvitations}},upsert=True)
        return "Okey"
    except:
        invitationsCollection.insert_one({"username":friend, "invitations":[username]})
        return "Okey"

def DbacceptFriendInvitation(username,friend):
    userInvitations = invitationsCollection.find_one({"username":username})["invitations"]
    userInvitations.remove(friend)
    invitationsCollection.find_one_and_update({"username":username},
        {"$set": {"invitations": userInvitations}},upsert=True)
    return "Okey"

# def authenticateUser(token= None):
# 	print("LLegamos a auth" + token)
# 	if(token != None):
# 		return friendsCollection.find_one({"app_token":token})
# 	return None


