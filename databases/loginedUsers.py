import datetime
from databases.users import usersDb

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

def setLoginedUsers():
    allUsers = usersDb.getAllUsers()
    dictionary = {} 
    for users in allUsers:
        if(users.get("token") != None):
            dictionary[users["username"]]=users.get("token")
    print(dictionary)
    return dictionary

class UsersTokens(Singleton):
    users = setLoginedUsers()

    def userLogin(self,user,token):
        print(self.users)
        self.users[user]=token

    def checkUserLogin(self,user,password):
        print("Checking user LOGIN", user)
        print (self.users)
        if user in self.users:
            print("Se checkea")
            return password == self.users.get(user)
        print("Fallo")
        return False


loginedUsers = UsersTokens()