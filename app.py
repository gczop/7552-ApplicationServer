from flask import Flask
from flask_restful import Resource, Api
import os



from flask_api import status
from api.routers.usersLoginRouter import UsersLoginRouter
from api.routers.usersSignUpRouter import UsersSignupRouter
from api.routers.friendsRouter import FriendsRouter, SpecificUserFriendsRouter
from api.routers.invitationsRouter import InvitationsRouter
from api.routers.peopleRouter import PeopleRouter, SinglePeopleRouter
from api.routers.notificationsRouter import NotificationsRouter
from api.routers.profilesRouter import ProfilesRouter
from api.routers.storiesRouter import StoriesRouter
from api.routers.flashStoriesRouter import FlashStoriesRouter
from api.routers.reactionsRouter import ReactionsRouter
from api.routers.commentsRouter import CommentsRouter
from api.routers.conversationsRouter import ConversationsRouter
from api.routers.pingRouter import PingRouter
from api.routers.statsRouter import StatsRouter
from logger.log import *

application = Flask(__name__)

api = Api(application, prefix="/api")

api.add_resource(UsersLoginRouter,'/users/login')
api.add_resource(UsersSignupRouter,'/users/signup')
api.add_resource(FriendsRouter,'/friends')
api.add_resource(SpecificUserFriendsRouter, '/friends/<string:username>')
api.add_resource(InvitationsRouter,'/invitations')
api.add_resource(PeopleRouter,'/people')
api.add_resource(SinglePeopleRouter,'/people/<string:username>')
api.add_resource(NotificationsRouter,'/notifications')
api.add_resource(ProfilesRouter,'/profile')
api.add_resource(StoriesRouter,'/stories')
api.add_resource(FlashStoriesRouter,'/flashstories')
api.add_resource(ReactionsRouter,'/reactions')
api.add_resource(CommentsRouter,'/comments')
api.add_resource(ConversationsRouter,'/conversations')
#api.add_resource(ConversationsRouter,'/conversations/<string:conv_id>')
api.add_resource(PingRouter,'/ping')
api.add_resource(StatsRouter,'/stats')


# see https://flask-httpauth.readthedocs.io/en/latest/
# auth = HTTPBasicAuth()

# users = {
#     "admin": "root",
# }

# @auth.get_password
# def get_pw(username):
#     if username in users:
#         return users.get(username)
#     return None

# @application.route('/secret')
# @auth.login_required
# def secret_page():
#     return "Hello, %s!" % auth.username()



@application.route('/')
def hello_world():
    return "Hi, I'm root!"


if __name__ == '__main__':
	log("Starting server")
	application.run(host='0.0.0.0')
