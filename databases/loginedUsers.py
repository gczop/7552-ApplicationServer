import datetime
from databases.users import usersDb
import threading
from logger.log import *


def setLoginedUsers():
    logInfo("loginnedUsers- Setting logined users")
    allUsers = usersDb.getAllUsers()
    usersList = [] 
    for users in allUsers:
        if(users.get("token") != None):
            usersList.append((users['username'],users.get('token')))
    return usersList

users = setLoginedUsers()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UsersTokens(metaclass=Singleton):
    time = 0
    def userLogin(self,user,token):
        logDebug("loginnedUsers- User login: "+str(user)+", token: "+str(token))
        global users
        self.time = self.time + 1
        for connectedUser in users:
            if connectedUser[0]==user:
                users.remove(connectedUser)
                tempList = users
                del users
                users = tempList
                users.append((user,token))
                return
        users.append((user,token))
        return


    def checkUserLogin(self,user,password):
        logDebug("loginnedUsers- Checking users LOGIN "+str(user)+" "+str(password)+" "+str(time))
        for connectedUser in users:
            if connectedUser[0]==user:
                return connectedUser[1] == password
        logError("LOGINUSERS01", str(user))
        return False

def checkUserLogin(user,password):
    logDebug("loginnedUsers- Checking user LOGIN"+str(user))
    for connectedUser in users:
        if connectedUser[0]==user:
            return connectedUser[1] == password
    logDebug("Check failed")
    logErrorCode("LOGINUSERS01", str(user))
    return False

loginedUsers = UsersTokens()
