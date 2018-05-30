import os
import pymongo
from pymongo import ReturnDocument
from pymongo import MongoClient
from logger.log import *

import pymongo

MONGO_URL = os.environ.get('MONGODB_URI')
print(MONGO_URL)

if MONGO_URL:
    # Get a connection
    conn = pymongo.MongoClient(MONGO_URL)
    from urllib.parse import urlparse
    # Get the database
    log("Notifications DB in MONGO")
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    log("Notifications DB in localhost")
    conn = pymongo.MongoClient('localhost', 27017)
    #conn = pymongo.MongoClient('mongo', 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']


notificationsCollection = db.Notifications

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class NotificationsDb(Singleton):
    notificationsList = notificationsCollection

    def getUserNotifications(self,username):
        log("Getting "+str(username)+" notifications")
        try:
            return notificationsCollection.find_one({"username":username})["notifications"]
        except:
            return notificationsCollection.find_one_and_update({"username":username},
            {"$set": {"notifications": []}},upsert=True,return_document=ReturnDocument.AFTER)["notifications"]

   
notificationsDb = NotificationsDb()
