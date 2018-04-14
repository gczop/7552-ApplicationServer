import os
import uuid
import pymongo
import datetime
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
    print("Conectamos local2")
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['StoriesAppServer']


storiesCollection = db.Stories


"""    DATABASES JSONs DEFINITIONS

{   "_id" : ID autodefinido
    "username" : Nombre de usuario
    "date" : Fecha de la historia
    "createdAt" : Fecha de creacion
    "updatedAt" : Fecha de ultima edicion
    "storyInfo" : 
        {   "description" : 
            "state" : Public | Private
        }
    "reactions" :
        { "reacter" : "reaction" => "me gusta | no me gusta | me divierte | me aburre", ...}

}

comments {
    "storyID" : FK a _id de stories
    "content" : [
    "comments": {
        "_id"
        "user"
        "date"
        "message"
    }]
}

"""




class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class StoriesDb(Singleton):
    storiesList = storiesCollection

    def getUserLastNStories(username, number = 5):
        fromNewToOld = -1
        return self.storiesDb.find({"username":username},projection={'_id':False}).sort({"date":fromNewToOld}).limit(number)

    def addNewStory(username, storyInfo):
        storyDict = createStoryDocument(storyInfo)
        self.storiesDb.insert_one({"username":username,"storyDetail":storyDict, "createdAt":str(datetime.datetime.now()), "updatedAt":str(datetime.datetime.now()),"reactions": {}})
        return "Okey"

    def updateStory(username, updateInfo):
        storyDict = createStoryDocument(updateInfo)
        oldStoryInfo = self.storiesDb.find_one({"_id":updateInfo["storyId"]})
        if(oldStoryInfo == None):
            raise Exception("Story inexistente")
        updatedInfo = createdUpdatedDictionary(storyDict,oldStoryInfo)
        self.users.find_one_and_update({"_id":updateInfo["storyId"]},
            {"$set": {"storyDetail": updatedInfo, "updatedAt": str(datetime.datetime.now())}},upsert=True)

    def deleteStory(username, storyId):
        self.storiesDb.delete_one({"_id",storyId})
        return "Okey"

    def addStoryReaction(storyId, username ,reaction):
        reactionData = { "reacter": username , "reaction": reaction }
        self.storiesDb.find_one_and_update({"username": username} ,{"$push": {"reactions" : reactionData }} , projection={'_id':False} ,upsert=True)
        return "Okey"


def createStoryDocument(storyInfo):
    document = {}
    document["description"] = storyInfo["description"]
    document["state"]= storyInfo["state"]
    return document

def createdUpdatedDictionary(newInformation, oldInormation):
    update = []
    for fields in oldInormation:
        update[fields]= newInformation.get(fields) or oldInormation.get(fields)
    return update

def createReaction(username, reaction):
    return

storiesDb = StoriesDb()