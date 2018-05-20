import os
import uuid
import pymongo
import datetime
from pymongo import MongoClient

from databases.friends import friendsDb

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
    #conn = pymongo.MongoClient('mongo', 27017)#DOCKER-TAG
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
            "url" : 
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

    def getUserLastNStories(self, username, number = 5):
        fromNewToOld = -1
        friends = friendsDb.getUserFriends(username);
        friends.append(username);
        # print (friends,"\n\n")
        # print (list(self.storiesList.find()),"\n\n")
        return list(self.storiesList.find({ "username": {"$in" : friends }}).sort("createdAt",fromNewToOld).limit(number))

    def addNewStory(self, username, storyInfo):
        storyDict = createStoryDocument(storyInfo)
        id = str(uuid.uuid4())
        self.storiesList.insert_one({"_id":id , "username":username,"storyDetail":storyDict, "createdAt":str(datetime.datetime.now()), "updatedAt":str(datetime.datetime.now()),"reactions": {}})
        return id

    def updateStory(self, username, id, updateInfo):
        oldStoryInfo = self.storiesList.find_one({"_id":id})
        if(oldStoryInfo == None):
            raise Exception("Story inexistente")
        storyDict = updateInfo

        newData = createdUpdatedDictionary(storyDict,oldStoryInfo['storyDetail'])

        self.storiesList.find_one_and_update({"_id":id},
            {"$set": {"storyDetail": newData, "updatedAt": str(datetime.datetime.now())}},upsert=True)

    def deleteStory(self, id):
        self.storiesList.delete_one({"_id": id})
        return "Okey"

    def getStoryReactions(self, storyId):
        return self.storiesList.find_one({ "storyId": storyId })["reactions"]

    def addStoryReaction(self, storyId, username ,reaction):
        reactionData = { "reacter": username , "reaction": reaction }

        self.storiesList.find_one_and_update({"storyId": storyId} ,{"$push": {"reactions" : reactionData }} , projection={'_id':False} ,upsert=True)
        return "Okey"

    def deleteStoryReaction(self, storyId, username):
        self.storiesList.find_one_and_update({"storyId": storyId } ,{"$pull": {"reactions" : {"reacter": username} }})
        return "Okey"


def createStoryDocument(storyInfo):
    document = {}
    document["description"] = storyInfo["description"]
    document["title"] = storyInfo["title"]
    document["state"]= storyInfo["state"]
    document["url"]= storyInfo["url"]
    return document

def createdUpdatedDictionary(newInformation, oldInormation):
    update = {}
    for fields in oldInormation:
        update[fields] = newInformation.get(fields) or oldInormation.get(fields)
    return update

def createReaction(username, reaction):
    return

storiesDb = StoriesDb()
