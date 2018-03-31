import requests

def authenticateUserLogin(username,password):
	payload = {
  		"username": username,
  		"password": password
	}
	return requests.post('http://localhost:10010/api/token', data= payload)