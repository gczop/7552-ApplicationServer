from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from api.controllers.storiesController import getHomepageFeed, addNewStory, updateStory, removeStory, getSpecificUserStories, getLocationStories, getPublicStories
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers


from functools import wraps
from flask import request, Response




def authenticationFailed():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def tokenExpired():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'This TOken is no longer valid\n'
    'Please Re login', 409,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not usersDb.checkUserLogin(auth.username,auth.password):
            return authenticationFailed()
        if usersDb.checkTokenNotExpired(auth.username):
            return tokenExpired()
        return f(*args, **kwargs)
    return decorated


auth = HTTPBasicAuth()

@auth.verify_password
def get_token(username,password):
    return usersDb.checkUserLogin(username,password)



class StoriesRouter(Resource):

	@requires_auth
	def get(self):
		return getHomepageFeed(request)

	@requires_auth
	def post(self):
		return addNewStory(request)

	@requires_auth
	def put(self):
		return updateStory(request)

	@requires_auth
	def delete(self):
		return removeStory(request)
		
class SpecificStoriesRouter(Resource):
    @requires_auth
    def get(self, username):
        return getSpecificUserStories(username)

class GeolocationStoriesRouter(Resource):
    @requires_auth
    def get(self):
        return getLocationStories(request)

class PublicStoriesRouter(Resource):
    @requires_auth
    def get(self):
        return getPublicStories(request)

class PublicGeolocationStoriesRouter(Resource):
    @requires_auth
    def get(self):
        return getPublicGeoStories(request)



