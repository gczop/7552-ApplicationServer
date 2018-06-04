from logger.errorCodes import codeMap
import logging
logging.basicConfig(level=logging.DEBUG,filename='Log.log', format='%(asctime)s||%(levelname)s:%(message)s')

def logErrorCode(*args):
    message = "["+args[0]+"] "+codeMap[args[0]]
    if len(args)>1:
        for x in range(1,len(args)):
            identificador = "%"+str(x)+"$"
            valor = args[x]
            message = message.replace(identificador, valor)
    print ("[ERROR] "+message)
    logging.error(message)
    
def logError(message):
	print("[ERROR]"+message)
	logging.error(message)


def logInfo(message):
	print ("[INFO] "+message)
	logging.info(message)


def logDebug(message):
	print ("[DEBUG] "+message)
	logging.debug(message)


def logWarning(message):
	print ("[WARNING]"+message)
	logging.warning(message)


