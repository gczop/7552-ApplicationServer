
import json
from flask import request
import os,sys,inspect
from SharedServerRequests.userLogin import authenticateUserLogin
from databases.users import usersDb
from databases.loginedUsers import loginedUsers


def validateUserLogin(request):
		user,password,fbToken = getRequestData(request)
		if(password == None and fbToken == None):
			return {"Error": "Falta de informacion de login (Error code: 2)"}, 400
		if(password != None):
			response =  authenticateUserLogin(user,password)
		else:
			response =  authenticateUserLogin(user,fbToken)
		responseData = json.loads(response.text)
		try:
			responseData["code"]
			return {"Error": "Login Incorrecto (Error code: 3)"}, 401
		except:
			usersDb.registerUserToken(user,responseData["token"])
			loginedUsers.userLogin(user,responseData["token"])
			return {"Message": "Bienvenido {}".format(user), "Token":responseData["token"]}	



def getRequestData(request):
	data = json.loads(request.data)
	user = data.get("username")
	password = data.get("password")
	fbToken = data.get("fbToken")
	return user,password,fbToken