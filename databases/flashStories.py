import os
import uuid
import pymongo
import datetime
from pymongo import MongoClient
from logger.log import *
from config import *
from databases.friends import friendsDb

import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("flashStories - FlashStories DB found in MONGO")
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("flashStories - FlashStories DB found in localhost")
    #conn = pymongo.MongoClient('localhost', 27017)
    conn = pymongo.MongoClient(getMongoHost(), 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']

if 'TEST_ENV' in os.environ:
    logInfo("flashStories- TEST_ENV found in os.environ")
    deltatime = datetime.timedelta(seconds=1)
else:
    deltatime = datetime.timedelta(hours=4)


flashStoriesCollection = db.FlashStories


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

class FlashStoriesDb(Singleton):
    storiesList = flashStoriesCollection


    def garbageCollector(self):
        logInfo("Deleting garbage")
        deletionDate = datetime.datetime.now() - deltatime
        print ("deleeeeete: ", deletionDate)
        #Se compara strings porque el formato da para eso
        self.storiesList.remove({ "createdAt" : { "$lt" : str(deletionDate) }});

    def getUserLastNStories(self, username, number = 5):
        logDebug("Getting last stories for "+str(username))
        fromNewToOld = -1
        friends = friendsDb.getUserFriends(username);
        friends.append(username);
        # print (friends,"\n\n")
        # print (list(self.storiesList.find()),"\n\n")

        self.garbageCollector();

        return list(self.storiesList.find({ "username": {"$in" : friends }}).sort("createdAt",fromNewToOld).limit(number))

    def addNewStory(self, username, storyInfo):
        logDebug("Adding new story for user "+str(username))
        storyDict = createStoryDocument(storyInfo)
        id = str(uuid.uuid4())
        self.storiesList.insert_one({"_id":id , "username":username,"storyDetail":storyDict, "createdAt":str(datetime.datetime.now()), "updatedAt":str(datetime.datetime.now()),"reactions": {}})
        return id

    def updateStory(self, username, id, updateInfo):
        oldStoryInfo = self.storiesList.find_one({"_id":id})
        logDebug("Updating story "+str(id)+" from user "+str(username))
        if(oldStoryInfo == None):
            logErrorCode("FLASH01")
            raise Exception("Story inexistente")
        storyDict = updateInfo

        newData = createdUpdatedDictionary(storyDict,oldStoryInfo['storyDetail'])

        self.storiesList.find_one_and_update({"_id":id},
            {"$set": {"storyDetail": newData, "updatedAt": str(datetime.datetime.now())}},upsert=True)

    def deleteStory(self, id):
        self.storiesList.delete_one({"_id": id})
        logDebug("Deleting story "+str(id))
        return "Okey"

    def getStoryReactions(self, storyId):
        logDebug("Getting story reactions for story "+str(id))
        return self.storiesList.find_one({ "storyId": storyId })["reactions"]

    def addStoryReaction(self, storyId, username ,reaction):
        logDebug("Adding "+str(reaction)+" reaction from "+str(username)+" for story "+str(id))
        reactionData = { "reacter": username , "reaction": reaction }

        self.storiesList.find_one_and_update({"storyId": storyId} ,{"$push": {"reactions" : reactionData }} , projection={'_id':False} ,upsert=True)
        return "Okey"

    def deleteStoryReaction(self, storyId, username):
        logDebug("Deleting reaction from"+str(username)+" for story "+str(id))
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

flashStoriesDb = FlashStoriesDb()
