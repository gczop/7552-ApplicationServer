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
    logInfo("Notifications DB in MONGO")
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    logInfo("Notifications DB in localhost")
    conn = pymongo.MongoClient('localhost', 27017)
    #conn = pymongo.MongoClient('mongo', 27017)#DOCKER-TAG
    db = conn['StoriesAppServer']


authenticationCollection = db.Authentication

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class AuthenticationDb(Singleton):
    authenticationList = authenticationCollection

    def getAuthentication(self):
        try:
            auth = authenticationCollection.find_one({"data":"serverToken"})
            print(auth)
            return auth['user'], auth['token']
        except:
            return None, None

    def registerAuthentication(self,user,token):
        oldAuth = authenticationCollection.find_one_and_replace({"data":"serverToken"},{"data":"serverToken","user":user, "token":token})
        if(oldAuth == None):
            authenticationCollection.insert_one({"data":"serverToken","user":user, "token":token})
        

        

   
authenticationsDb = AuthenticationDb()
