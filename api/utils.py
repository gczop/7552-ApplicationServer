

def getRequestHeader(request,headerName):
    user = request.headers.get(headerName)
    return user

