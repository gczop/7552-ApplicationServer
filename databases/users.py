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
    print("Conectamos local1")
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['StoriesAppServer']


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
        a = self.users.find(projection ={'_id':False, "username":True, "token":True})
        print(a)
        return a

    def registerUserToken(self,user, token):
        self.users.find_one_and_update({"username":user},
            {"$set": {"token": token}},upsert=True)

    def addNewUser(self,username= None,token= None):
        if(username == None):
            return
        self.users.insert_one({"username":username,"token":token})

    def getUserProfile(self, username):
        return self.users.find_one({"username": username})["personalInformation"]

    def updateUserProfile(self, username, updatedInfo):
        oldInformation = self.users.find_one({"username": username})["personalInformation"]
        update = createdUpdatedDictionary(updatedInfo,oldInformation)
        self.users.find_one_and_update({"username":user},
            {"$set": {"personalInformation": update}},upsert=True)


    def searchForSingleUser(self,username):
        return self.users.find_one({"username": username},projection={'_id':False})

    def searchForUsers(self,username):
        matchCursor = self.users.find({"username" : {'$regex' : ".*"+username+".*"}},projection={'_id':False, 'username':True})
        matchList = []
        for match in matchCursor:
           matchList.append(match)
        return match

    def authenticateUser(self,token= None):
        print("LLegamos a auth" + token)
        if(token != None):
            return self.users.find_one({"token":token})
        return None

usersDb = UsersDB()


def createdUpdatedDictionary(newInformation, oldInormation):
    update = []
    for fields in oldInormation:
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




