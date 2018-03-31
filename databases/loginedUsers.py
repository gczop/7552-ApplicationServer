import datetime


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class UsersTokens(Singleton):
    users = {}

    def userLogin(self,user,token):
    	self.users[user]=[token,datetime.datetime.now()+datetime.timedelta(hours=3)]
    	print self.users

    def checkUserLogin(self,user):
    	print self.users
    	if user in self.users:
    		return self.users.get(user)[0]
    	return None

loginedUsers = UsersTokens()