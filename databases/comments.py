import os
import uuid
import pymongo
import datetime
from pymongo import MongoClient
from logger.log import *

import pymongo
import uuid

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    log("Comments DB in MONGO")
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    log("Comments DB in localhost")
    conn = pymongo.MongoClient('localhost', 27017)
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
        log("Adding comment")
        self.commentsList.insert_one({"storyId": storyId , "content": []})

    def addNewComment(self, storyID, username, comment):
        log("Adding new comment: "+str(comment))
        storyComment = createComment(username, comment)

        print (storyComment)
        #self.commentsList.insert_one({"storyId":storyID},{"$push": {"content": storyComment }})
        self.commentsList.find_one_and_update({"storyId": storyID}, {"$push": {"content": storyComment}})
        return storyComment["_id"]

    def removeComment(self, storyId, commentID):
        log("Removing comment "+str(commentID)+ " from story "+str(storyID))
        self.commentsList.find_one_and_update({"storyId" : storyId} , { "$pull" : { "content" : {"_id": commentID } }})
        return "Okey"

    def getStoryComments(self, storyId):
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
