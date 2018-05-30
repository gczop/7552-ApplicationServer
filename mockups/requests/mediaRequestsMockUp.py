import requests
import os
from mockups.requests.mediaSharedServerTableMockUp import mediaDb
import datetime

def uploadNewFile(username,fileUrl):
    payload = {
        "id": username,
        "createdTime": str(datetime.datetime.now()),
        "size": "anySize",
        "filename": "noName",
        "resource": fileUrl
    }
    return mediaDb.addNewFile(payload)

def getFirebaseUrl(url):
    return mediaDb.getFirbase(url)