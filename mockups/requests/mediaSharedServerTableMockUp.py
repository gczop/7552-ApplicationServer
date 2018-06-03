import requests
import os
import json
import hashlib

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class UserSingupSharedServer(Singleton):
    files = {}
    ids = 1

    def getFirbase(self,hash):
        if(hash == None):
            return HttpReqMockUp({
                            "message": 'Hash faltante'
                        },400)
        if hash  in self.files:
            return HttpReqMockUp({
                "resource": self.files[hash]['resource']
                })
        return HttpReqMockUp({"message":"Inexistent file"},400)

    def addNewFile(self,payload):
        hashObj = hashlib.md5((payload['id']+payload['createdTime']).encode())
        hashString = hashObj.hexdigest()
        self.files[hashString] = payload
        return HttpReqMockUp({
            '_rev': hashString
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



mediaDb = UserSingupSharedServer()

def generateNewUser(username,password,fbToken,ids):
    return {
                "id": ids,
                "_rev": None,
                "applicationOwner": "String",
                "username": username,
                "password": password or fbToken
        }
