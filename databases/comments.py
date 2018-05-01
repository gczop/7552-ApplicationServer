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
    print("Conectamos local6")
    conn = pymongo.MongoClient('localhost', 27017)
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
        self.commentsList.insert_one({"storyId": storyId, "content": []})

    def addNewComment(self, storyID, username, comment):
        storyComment = createComment(username, comment)
        self.commentsList.insert_one_and_update({"stroryId":storyID},{"$push": {"content": {storyComment}}})
        return "Okey"

    def removeComment(self, storyId, commentID):
        self.commentsList.find_one_and_update({"_id" : storyId} , { "$pull" : { "_id" : commentID}})
        return "Okey"



commentsDb = CommentsDb()
