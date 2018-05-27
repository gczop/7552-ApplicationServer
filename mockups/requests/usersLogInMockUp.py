import requests
import os
from mockups.requests.usersSharedServerTableMockUp import usersDb
from logger.log import *

def authenticateUserLogin(username,password):
    log("User login mockup")
    return usersDb.loginUser(username,password)
