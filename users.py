from mongoengine import *

connect('StoriesAppServer')

class User(Document):
	email = StringField(required = true)
	first_name = StringField(max_length = 50)
	last_name = StringField(max_length = 50)
	app_token = StringField(max_length = 20)
	token_experation = DateTimeField()



def authenticate_user(token= None, email= None, password= None):
	if(token != None):
		for users in User.objects(token = token):
			return users
	elif(email != None & password != None):
		for users in User.objects(email= email, password= password)
			return users
	return None


