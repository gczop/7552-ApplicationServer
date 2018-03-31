import requests

def registerNewUser(username,password,fbToken):
	payload = {
 	 "username": username,
 	 "password": password,
 	 "facebookAuthToken": fbToken
	}
	return requests.post('http://localhost:10010/api/authorize', data= payload)