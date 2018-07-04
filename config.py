USE_DOCKER = False

def getMongoHost():
	if (USE_DOCKER):
		return "mongo"
	return "localhost"

def getSharedServerHost():
	if (USE_DOCKER):
		return "http://web-shared:10010"
	return "http://127.0.0.1:10010"

