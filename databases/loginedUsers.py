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


class Singleton(type):
    _instances = {}
    time = 0
    users = setLoginedUsers()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UsersTokens(metaclass=Singleton):

    def userLogin(self,user,token):
        print('Changin tokenJJJJJJ',token ,user, threading.get_ident(), self.time)
        self.time = self.time + 1
        for connectedUser in self.users:
            if connectedUser[0]==user:
                self.users.remove(connectedUser)
                self.users.append((user,token))
                return
        self.users.append((user,token))
        return


    def checkUserLogin(self,user,password):
        print("Checking user LOGIN", user, password, self.time)
        print (self.users,threading.get_ident(),self)
        for connectedUser in self.users:
            if connectedUser[0]==user:
                return connectedUser[1] == password
        print("Fallo")
        return False


loginedUsers = UsersTokens()