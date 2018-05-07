import datetime
from databases.users import usersDb

def setLoginedUsers():
    allUsers = usersDb.getAllUsers()
    dictionary = {} 
    for users in allUsers:
        if(users.get("token") != None):
            print('Changing Token now HHHHHHH', users.get('token'))
            dictionary[users["username"]]=[users.get("token")]
    print(dictionary)
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
        if user in self.users:
            self.users[user].pop()
            self.users[user].append(token)
            return
        self.users[user]=[token]


    def checkUserLogin(self,user,password):
        print("Checking user LOGIN", user, password)
        print (self.users)
        if user in self.users:
            print("Se checkea")
            print (self.users.get(user))
            return password == self.users.get(user)[0]
        print("Fallo")
        return False


loginedUsers = UsersTokens()