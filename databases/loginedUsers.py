import datetime
from databases.users import usersDb

def setLoginedUsers():
    allUsers = usersDb.getAllUsers()
    usersList = [] 
    for users in allUsers:
        if(users.get("token") != None):
            print('Changing Token now HHHHHHH', users.get('token'))
            usersList.append(users['username'],users.get('token'))
    print(usersList)
    return dictionary

class Singleton(object):
    _instance = None
    users = setLoginedUsers()
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance



class UsersTokens(Singleton):
    

    def userLogin(self,user,token):
        print('Changin tokenJJJJJJ',token ,user)
        for connectedUser in self.users:
            if connectedUser[0]==user:
                self.users.remove(connectedUser)
                self.users.append((user,token))
                return
        self.users.append((user,token))
        return


    def checkUserLogin(self,user,password):
        print("Checking user LOGIN", user, password)
        print (self.users)
        for connectedUser in self.users:
            if connectedUser[0]==user:
                return connectedUser[1] == password
        print("Fallo")
        return False


loginedUsers = UsersTokens()