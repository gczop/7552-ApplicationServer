import requests
import os
from mockups.requests.usersSharedServerTableMockUp import usersDb

def authenticateUserLogin(username,password):
    return usersDb.loginUser(username,password)