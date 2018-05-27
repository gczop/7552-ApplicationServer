from logger.errorCodes import codeMap

def logError(*args):
    message = "["+args[0]+"] "+codeMap[args[0]]
    if len(args)>1:
        for x in range(1,len(args)):
            identificador = "%"+str(x)+"$"
            valor = args[x]
            message = message.replace(identificador, valor)
    print (message)
    writeMessage(message)
    

def log(message):
	print (message)
	writeMessage(message)


def writeMessage(message):
	with open ("Log.txt", "a+") as outputFile:
		outputFile.write(message)
		outputFile.write("\n")
	outputFile.close()
