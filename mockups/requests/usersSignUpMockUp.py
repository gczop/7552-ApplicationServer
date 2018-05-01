import requests
import os
from mockups.requests.usersSharedServerTableMockUp import usersDb


def registerNewUser(username,password,fbToken):
	return usersDb.signUpNewUser(username,password,fbToken)



