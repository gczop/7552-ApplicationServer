import os
import pymongo
from pymongo import ReturnDocument
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
    print("Conectamos local3")
    conn = pymongo.MongoClient('localhost', 27017)
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
        try:
            return notificationsCollection.find_one({"username":username})["notifications"]
        except:
            return notificationsCollection.find_one_and_update({"username":username},
            {"$set": {"notifications": []}},upsert=True,return_document=ReturnDocument.AFTER)["notifications"]

   
notificationsDb = NotificationsDb()
