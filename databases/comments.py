import os
import uuid
import pymongo
import datetime
from pymongo import MongoClient
from logger.log import *
from databases.stories import storiesDb
from config import *
import pymongo
import uuid

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    logInfo("Comments DB in MONGO")
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("Comments DB in localhost")
    conn = pymongo.MongoClient(getMongoHost(), 27017)
    #conn = pymongo.MongoClient('mongo', 27017) #DOCKER-TAG
    db = conn['StoriesAppServer']


commentsCollection = db.Comments


"""    DATABASES JSONs DEFINITIONS

comments {
    "storyId" : FK a _id de stories
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

class CommentsDb(Singleton):
    commentsList = commentsCollection

    def addComments(self, storyId):
        logDebug("comments- Adding comment to story "+str(storyId))
        self.commentsList.insert_one({"storyId": storyId , "content": []})

    def addNewComment(self, storyID, username, comment):
        logDebug("comments-"+str(username)+" adding comment: "+str(comment)+" to story "+str(storyID))
        storyComment = createComment(username, comment)
        logInfo("comments- comment:"+str(storyComment))
        #self.commentsList.insert_one({"storyId":storyID},{"$push": {"content": storyComment }})
        self.commentsList.find_one_and_update({"storyId": storyID}, {"$push": {"content": storyComment}})
        storiesDb.addNewComment(storyID)
        return storyComment["_id"]

    def removeComment(self, storyId, commentID):
        logDebug("comments- Removing comment "+str(commentID)+ " from story "+str(storyId))
        self.commentsList.find_one_and_update({"storyId" : storyId} , { "$pull" : { "content" : {"_id": commentID } }})
        return "Okey"

    def getStoryComments(self, storyId):
        logDebug("comments-Getting comments from story "+str(storyId))
        # return self.commentsList.find_one({ "storyId" : storyId})#.sort("date",fromNewToOld))
        return self.commentsList.find_one({"storyId": storyId})["content"][::-1]

def createComment(username, comment):
    return {
        "_id" : str(uuid.uuid4()),
        "user": username,
        "date": str(datetime.datetime.now()),
        "message": comment
    }


commentsDb = CommentsDb()
