import requests
import os
import json

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class UserSingupSharedServer(Singleton):
    users = {}
    ids = 1

    def signUpNewUser(self,username,password,fbToken):
        if(password == None and fbToken == None):
            return HttpReqMockUp({
                            "code":400,
                            "message": 'Parametros de signup faltantes'
                        })
        if username in self.users:
            return HttpReqMockUp({"code":401, "message":"User Already registerd"})
        newUser = generateNewUser(username,password,fbToken,self.ids)
        self.users[username] = newUser
        self.ids +=1
        return HttpReqMockUp({
                                    'id': newUser['id'],
                                    "_rev": newUser["_rev"],
                                    "applicationOwner": newUser["applicationOwner"],
                                    "username": newUser["username"]
                                })

    def loginUser(self,username,password):
        if username not in self.users or self.users[username]["password"] != password:
            return HttpReqMockUp({
                            "code":401,
                            "message": "Datos de login incorrectos"
                        })
        else:
            self.users[username]["token"]= "eTKhUrPGek"
            return HttpReqMockUp({
                            "token": "eTKhUrPGek"
                        })
        # return 0


    def registerUserToken(self, username, token):
        if username not in self.users:
            return HttpReqMockUp({
                "code":401,
                "message": "Datos de register incorrectos"
            })
        else:
            self.users[username]["token"]= token
            return HttpReqMockUp({
                "token": token
            })
    
class HttpReqMockUp(object):
    text = ""
    def __init__(self,content):
        self.text = json.dumps(content)


#         if username in self.users:
#             return {"code":401, "message":"User Already registerd"}
#         newUser = generateNewUser(username,password,fbToken,self.ids)
#         self.users[username] = newUser
#         self.ids +=1
#         return newUser
# # userInfo = self.users[username]
        # return {
        # 	"id": userInfo["id"],
        # 	"_rev": userInfo["_rev"],
     #    	"applicationOwner": userInfo["applicationOwner"],
     #    	"username": userInfo["username"],
        # }
# 	def loginUser(self,username,password):
# 		if username not in self.users or self.users[username]["password"] != password:
# 			return {
# 			    "code": 401,
# 			    "message": "Datos de login incorrectos"
# 			}
# 		else:
# 			self.users[username]["token"]= "eTKhUrPGek"
# 			return {
#     			
# 			}



usersDb = UserSingupSharedServer()

def generateNewUser(username,password,fbToken,ids):
    return {
                "id": ids,
                "_rev": None,
                "applicationOwner": "String",
                "username": username,
                "password": password or fbToken
        }
