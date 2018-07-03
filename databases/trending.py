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


trendingCollection = db.TrendingRegister
postsSample = 100
reactionsSample = 1000


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class TrendingDb(Singleton):
    postsLists = trendingCollection

    def setPostRegister(self):
        try:
            postRegister =trendingCollection.find_one({"variable":"posts"})
            postRegister["postsAuthors"]
        except:
            trendingCollection.insert_one({"variable":"posts", "postsAuthors":[]})

    def setReactionsRegister(self):
        try:
            postRegister =trendingCollection.find_one({"variable":"reactions"})
            postRegister["reactionReceiver"]
        except:
            trendingCollection.insert_one({"variable":"reactions", "reactionReceiver":[]})


    def registerNewPost(self,username):
        postRegister = trendingCollection.find_one({"variable":"posts"})["postsAuthors"]
        if(len(postRegister)>=postsSample):
            postRegister.pop(0)
        postRegister.append(username)
        trendingCollection.find_one_and_update({"variable":"posts"},{"$set": {"postsAuthors":postRegister}})

    def registerNewReaction(self,username):
        reactionsRegister = trendingCollection.find_one({"variable":"reactions"})["reactionReceiver"]
        if(len(reactionsRegister)>=postsSample):
            reactionsRegister.pop(0)
        reactionsRegister.append(username)
        trendingCollection.find_one_and_update({"variable":"reactions"},{"$set": {"reactionReceiver":reactionsRegister}})

    def getPostsProportion(self,username):
        postRegister = trendingCollection.find_one({"variable":"posts"})["postsAuthors"]
        return postRegister.count(username)/len(postRegister)*15

    def getReactionsProportion(self,username):
        reactionsRegister = trendingCollection.find_one({"variable":"reactions"})["reactionReceiver"]
        return reactionsRegister.count(username)/len(reactionsRegister)*35
        

   
trendingsDb = TrendingDb()
trendingsDb.setReactionsRegister()
trendingsDb.setPostRegister()
