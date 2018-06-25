import os
import re

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class UsersDBMockUp(Singleton):
    users = {}

    def getAllUsers(self):
        return self.users.values()

    def registerUserToken(self,user, token):
    	self.users[user]["token"] = token

    def addNewUser(self,username= None,token= None,fbToken=False):
        if(username == None):
            return
        self.users[username]= {
        	"username": username,
        	"token": token
        }

    def getUserProfile(self, username):
        return self.username[username]

    def updateUserProfile(self, username, updatedInfo):
        oldInformation = self.users[username]
        update = createdUpdatedDictionary(updatedInfo,oldInformation)
        self.users[username]= update


    def searchForSingleUser(self,username):
        return self.users[username]

    def searchForUsers(self,username):
    	matches = []
    	for key, value in self.users:
    		if username in key:
    			matches.append(self.users[key])
    	return matches

    def authenticateUser(self,username,token= None):
        if(token != None):
        	if(self.users[username]["token"]== token)
            	return self.users[username]
        return None

usersDb = UsersDBMockUp()


def createdUpdatedDictionary(newInformation, oldInormation):
    update = []
    for fields in oldInormation:
        update[fields]= newInformation.get(fields) or oldInormation.get(fields)
    return update




