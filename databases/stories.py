import os
import uuid
import pymongo
import datetime
from pymongo import MongoClient
from logger.log import *
from databases.friends import friendsDb
from databases.trending import trendingsDb
from config import *
import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    logInfo("stories- Stories DB in MONGO")
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("stories- Stories DB in localhost")
    #conn = pymongo.MongoClient('localhost', 27017)
    conn = pymongo.MongoClient(getMongoHost(), 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']


storiesCollection = db.Stories
usersCollection = db.User


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

    def getLastNPublicStories(self, username, number = 5):
        logDebug("stories- Retrieving last "+str(number)+ "stories")
        fromNewToOld = -1
        # print (friends,"\n\n")
        # print (list(self.storiesList.find()),"\n\n")
        return orderStoriesRelevance(username, list(self.storiesList.find({ "storyDetail.state": "Public"}).sort("createdAt",fromNewToOld).limit(number)))

    def getUserLastNGeoPublicStories(self, username, number = 5):
        logDebug("stories- Retrieving last "+str(number)+ "stories")
        fromNewToOld = -1
        friends = friendsDb.getUserFriends(username);
        friends.append(username);
        # print (friends,"\n\n")
        # print (list(self.storiesList.find()),"\n\n")
        return list(self.storiesList.find({  "storyDetail.state": "Public", "storyDetail.lat": {"$ne": None}, "storyDetail.long": {"$ne": None},}).sort("createdAt",fromNewToOld).limit(number))


    def getStoryOwner(self, storyId):
        return self.storiesList.find_one({"_id": storyId}).get("username")

    def getUserLastNGeoStories(self, username, number = 5):
        logDebug("stories- Retrieving last "+str(number)+ "stories")
        fromNewToOld = -1
        friends = friendsDb.getUserFriends(username);
        friends.append(username);
        # print (friends,"\n\n")
        # print (list(self.storiesList.find()),"\n\n")
        return list(self.storiesList.find({ "username": {"$in" : friends }, "storyDetail.lat": {"$ne": None}, "storyDetail.long": {"$ne": None},}).sort("createdAt",fromNewToOld).limit(number))


    def addNewComment(self,storyId):
        storiesCollection.update({ "_id" : storyId }, { "$inc": {"comments": 1}})

    def addNewLike(self,storyId):
        storiesCollection.update({ "_id" : storyId }, { "$inc": {"likes": 1}})


    def getUserLastNStories(self, username, number = 5):
        logDebug("stories- Retrieving last "+str(number)+ "stories")
        fromNewToOld = -1
        friends = friendsDb.getUserFriends(username);
        friends.append(username);
        # print (friends,"\n\n")
        # print (list(self.storiesList.find()),"\n\n")
        return orderStoriesRelevance(username, list(self.storiesList.find({ "username": {"$in" : friends }}).sort("createdAt",fromNewToOld).limit(number)))

    def getUserStories(self, user ,userRequested, number = 5):
        logDebug("stories- Retrieving last "+str(number)+ "stories from "+ userRequested)
        friends = friendsDb.getUserFriends(userRequested);
        friends.append(userRequested);
        fromNewToOld = -1
        if(not user in friends):
            return list(self.storiesList.find({ "username": userRequested , "storyDetail.state": "Public"}).sort("createdAt",fromNewToOld).limit(number))    
        return list(self.storiesList.find({ "username": userRequested}).sort("createdAt",fromNewToOld).limit(number))

    def addNewStory(self, username, storyInfo):
        logDebug("stories- Adding new story for user "+str(username))
        storyDict = createStoryDocument(storyInfo)
        trendingsDb.registerNewPost(username)
        id = str(uuid.uuid4())
        self.storiesList.insert_one({"_id":id , "username":username,"likes": 0, "comments": 0,"storyDetail":storyDict, "createdAt":str(datetime.datetime.now()), "updatedAt":str(datetime.datetime.now()),"reactions": []})
        return id

    def updateStory(self, username, id, updateInfo):
        logDebug("stories- Updating story "+str(id)+" for user "+str(username))
        oldStoryInfo = self.storiesList.find_one({"_id":id})
        if(oldStoryInfo == None):
            logErrorCode("STORIES01")
            raise Exception("Story inexistente")
        storyDict = updateInfo

        newData = createdUpdatedDictionary(storyDict,oldStoryInfo['storyDetail'])

        self.storiesList.find_one_and_update({"_id":id},
            {"$set": {"storyDetail": newData, "updatedAt": str(datetime.datetime.now())}},upsert=True)

    def deleteStory(self, id):
        logDebug("stories- Deleting story "+str(id))
        self.storiesList.delete_one({"_id": id})
        return "Okey"

    def getStoryReactions(self, storyId):
        logDebug("stories- Getting reactions for story: "+str(storyId))
        return self.storiesList.find_one({ "_id": storyId })["reactions"]

    def addStoryReaction(self, storyId, username ,reaction):
        logDebug("stories- Adding reaction to story")
        reactionData = { "reacter": username , "reaction": reaction }
        postOwner = self.storiesList.find_one({"_id":storyId})["username"]
        trendingsDb.registerNewReaction(postOwner)
        self.storiesList.find_one_and_update({"_id": storyId} ,{"$push": {"reactions" : reactionData }} , projection={'_id':False} ,upsert=True)
        self.addNewLike(storyId)
        return "Okey"

    def deleteStoryReaction(self, storyId, username):
        logDebug("stories- Deleting reaction from "+str(username)+" for story: "+str(storyId))
        self.storiesList.find_one_and_update({"_id": storyId } ,{"$pull": {"reactions" : {"reacter": username} }})
        return "Okey"


def createStoryDocument(storyInfo):
    document = {}
    document["description"] = storyInfo["description"]
    document["title"] = storyInfo["title"]
    document["state"]= storyInfo["state"]
    document["url"]= storyInfo["url"]
    document["lat"]= storyInfo["lat"]
    document["long"]= storyInfo["long"]
    return document

def createdUpdatedDictionary(newInformation, oldInormation):
    update = {}
    for fields in oldInormation:
        update[fields] = newInformation.get(fields) or oldInormation.get(fields)
    return update

def createReaction(username, reaction):
    return

def getUserRelevance(username, otherUsername):
        userInterests = usersCollection.find_one({"username":username}).get("userInterests")
        if(len(userInterests)*25 == 0):
            return 1
        return userInterests.count(otherUsername)/len(userInterests)*25

def orderStoriesRelevance(user, stories):
    likesImportance = 0.7
    commentsImportance = 0.5
    print("AAAAAAASSDASDHJSKBDBJK")
    for story in stories:
        print(story)
        story["importance"] = story["likes"]* likesImportance + story["comments"]* commentsImportance
        story["importance"] += trendingsDb.getPostsProportion(story["username"]) + trendingsDb.getReactionsProportion(story["username"])
        story["importance"] *= getUserRelevance(user,story["username"])
    newlist = sorted(stories, key=lambda k: k['importance'],reverse= True)
    return newlist
storiesDb = StoriesDb()
