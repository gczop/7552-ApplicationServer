import requests
import os
from mockups.requests.usersSharedServerTableMockUp import usersDb
from logger.log import *

def registerNewUser(username,password,fbToken):
    logInfo("Mocking user signup")
    return usersDb.signUpNewUser(username,password,fbToken)



