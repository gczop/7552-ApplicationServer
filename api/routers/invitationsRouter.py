from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from flask import request
from SharedServerRequests.userLogin import *
from databases.users import *
from databases.loginedUsers import loginedUsers
from api.controllers.invitationsController import getUserInvitations, addFriendInvitation, acceptFriendInvitation

auth = HTTPBasicAuth()

@auth.get_password
def get_token(username):
    return loginedUsers.checkUserLogin(username)



class InvitationsRouter(Resource):

	@auth.login_required
	def get(self):
		return getUserInvitations(request)

	@auth.login_required
	def post(self):
		return addFriendInvitation(request)

	@auth.login_required
	def put(self):
		return acceptFriendInvitation(request)		