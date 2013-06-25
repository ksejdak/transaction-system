import string

class CommandParser(object):

	def __init__(self):
		self.__destinationServer = ""
		self.__commandType = ""
	
	def parse(self, message, transactionId):
		message.rstrip()
		words = string.split(message, ":")
		
		if(words[0] == "BT" or words[0] == "bt"):
			self.__destinationServer = ""
			self.__commandType = "begin"
			return "BT:" + transactionId
		elif(words[0] == "R" or words[0] == "r"):
			if(len(words) == 2):
				self.__destinationServer = words[1]
				self.__commandType = "read"
				return "R:" + transactionId
			else:
				self.__commandType = "invalid"
				return "invalid"
		elif(words[0] == "W" or words[0] == "w"):
			if(len(words) == 3):
				self.__destinationServer = words[1]
				self.__commandType = "write"
				return "W:" + transactionId + ":" + words[2]
			else:
				self.__commandType = "invalid"
				return "invalid"
		elif(words[0] == "C" or words[0] == "c"):
			self.__destinationServer = ""
			self.__commandType = "commit"
			return "C:" + transactionId
		elif(words[0] == "A" or words[0] == "a"):
			self.__destinationServer = ""
			self.__commandType = "abort"
			return "A:" + transactionId
		else:
			self.__commandType = "invalid"
			return "invalid"
	
	def getDestinationServer(self):
		self.__destinationServer = self.__destinationServer.rstrip()
		return self.__destinationServer
	
	def getCommandType(self):
		return self.__commandType