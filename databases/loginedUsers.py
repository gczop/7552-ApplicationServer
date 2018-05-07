import datetime
from databases.users import usersDb
import threading


def setLoginedUsers():
    allUsers = usersDb.getAllUsers()
    usersList = [] 
    for users in allUsers:
        if(users.get("token") != None):
            print('Changing Token now HHHHHHH', users.get('token'))
            usersList.append((users['username'],users.get('token')))
    print(usersList)
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
        global users
        print('Changin tokenJJJJJJ',token ,user, threading.get_ident(), self.time)
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
        print("Checking user LOGIN", user, password, self.time)
        print (users,threading.get_ident(),self)
        for connectedUser in users:
            if connectedUser[0]==user:
                return connectedUser[1] == password
        print("Fallo")
        return False

def checkUserLogin(user,password):
    print("Checking user LOGIN", user, password)
    print (users,threading.get_ident())
    for connectedUser in users:
        if connectedUser[0]==user:
            return connectedUser[1] == password
    print("Fallo")
    return False

loginedUsers = UsersTokens()