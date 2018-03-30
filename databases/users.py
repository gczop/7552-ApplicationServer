import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.StoriesAppServer
userCollection = db.User




def authenticate_user(token= None, email= None, password= None):
	print("LLegamos a auth" + token + email + password)
	if(token != None):
		return userCollection.find_one({"app_token":token})
	return None


