import os
import pymongo
from datetime import datetime, timedelta
from pymongo import MongoClient
from logger.log import *

import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("users- Users DB in MONGO")
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("users- Users DB in localhost")
    conn = pymongo.MongoClient('localhost', 27017)
    #conn = pymongo.MongoClient('mongo', 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']

# users:{
#     "username": username,
#     "fisrt_name": name,
#     "last_name": last name,
#     "gender": gender,
#     "age": age,
#     "birthday": birthday
# }
userCollection = db.User

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class UsersDB(Singleton):
    users = userCollection

    def getAllUsers(self):
        logDebug("users- Getting all users")
        a = self.users.find(projection ={'_id':False, "username":True, "token":True})
        return a

    def registerUserToken(self,user, token):
        logDebug("users-Registering user token")
        if(self.users.find_one({"username":user}) != None):
            self.users.find_one_and_update({"username":user},
                {"$set": {"token": token, "expiration": datetime.now()+timedelta(hours=12)}},upsert=True)
        else:
            self.addNewUser(user,token)

    def addNewUser(self,username= None,token= None,personalInfo=None):
        if(username == None):
            logError("users-No username received")
            return
        logDebug("Adding new user: "+username)
        self.users.insert_one({"username":username,"token":token, "expiration": datetime.now()+timedelta(hours=12),"personalInformation": personalInfo or {}})

    def getUserProfile(self, username):
        logDebug("users-Getting "+str(username)+" profile")
        return self.users.find_one({"username": username})["personalInformation"]

    def updateUserProfile(self, username, updatedInfo):
        logDebug("users-Updating "+str(username)+ " profile")
        oldInformation = self.users.find_one({"username": username}).get("personalInformation")
        update = createdUpdatedDictionary(updatedInfo,oldInformation)
        self.users.find_one_and_update({"username":username},
            {"$set": {"personalInformation": update}},upsert=True)

    def checkTokenNotExpired(self,username):
        return self.users.find_one({'username':username}).get('expiration') < datetime.now()

    def checkUserLogin(self,username,password):
        logDebug("users-Checking "+str(username)+ " login")
        return self.users.find_one({'username':username}).get('token') == password


    def searchForSingleUser(self,username):
        logDebug("users-Searching "+str(username)+ " in DB")
        return self.users.find_one({"username": username},projection={'_id':False})

    def searchForUsers(self,username):
        logDebug("users-Searching users in DB: "+str(username))
        matchCursor = self.users.find({"username" : {'$regex' : ".*"+username+".*"}},projection={'_id':False, 'username':True})
        matchList = []
        for match in matchCursor:
           matchList.append(match)
        return matchList

    def authenticateUser(self,username,token= None):
        logDebug("users-Authenticating: "+str(username))
        if(token != None):
            return self.users.find_one({
                "token":token,
                "username":username
                })
        logDebug("No token found")
        return None

usersDb = UsersDB()


def createdUpdatedDictionary(newInformation, oldInormation):
    update = {}
    for fields in newInformation:
        update[fields]= newInformation.get(fields) or oldInormation.get(fields)
    return update

# def DbSearchForUsers(username):

#     matchCursor = userCollection.find({"username" : {'$regex' : ".*"+username+".*"}},projection={'_id':False, 'username':True})
#     matchList = []
#     for match in matchCursor:
#         matchList.append(match)
#     return match
    
# def DbSearchForSingleUser(username):
#     return userCollection.find_one({"username": username},projection={'_id':False})

# def DbAddNewUser(username= None,token= None):
#     if(username == None):
#         return
#     userCollection.insert_one({"username":username,"token":token})




