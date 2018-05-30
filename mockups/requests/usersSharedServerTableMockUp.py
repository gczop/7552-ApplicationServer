import requests
import os
import json
from logger.log import *

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
        log("Mocking user signup")
        if(password == None and fbToken == None):
            logError("MOCK01")
            return HttpReqMockUp({
                            "message": 'Parametros de signup faltantes'
                        },400)
        if username in self.users:
            logError("MOCK02", username)
            return HttpReqMockUp({"message":"User Already registerd"},401)
        newUser = generateNewUser(username,password,fbToken,self.ids)
        self.users[username] = newUser
        self.ids +=1
        log("Mocking new user")
        return HttpReqMockUp({
                                    'id': newUser['id'],
                                    "_rev": newUser["_rev"],
                                    "applicationOwner": newUser["applicationOwner"],
                                    "username": newUser["username"]
                                })

    def loginUser(self,username,password):
        if username not in self.users or self.users[username]["password"] != password:
            logError("MOCK03")
            return HttpReqMockUp({
                            "message": "Datos de login incorrectos"
                        },401)
        else:
            log("Mocking succesful login")
            self.users[username]["token"]= "eTKhUrPGek"
            return HttpReqMockUp({
                            "token": "eTKhUrPGek"
                        })


    def registerUserToken(self, username, token):
        if username not in self.users:
            logError("MOCK04", username)
            return HttpReqMockUp({
                "message": "Datos de register incorrectos"
            },401)
        else:
            log("Mocking user registry")
            self.users[username]["token"]= token
            return HttpReqMockUp({
                "token": token
            })
    
class HttpReqMockUp(object):
    text = ""
    status_code =0
    def __init__(self,content, code =200):
        self.text = json.dumps(content)
        self.status_code = code


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
