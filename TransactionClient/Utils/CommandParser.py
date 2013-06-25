import string
import random

class CommandParser(object):

	def __init__(self):
		self.__destinationServer = ""
		self.__commandType = ""
	
	def parse(self, message):
		#message.strip()
		words = string.split(message, ":")
		
		if(words[0] == "BT" or words[0] == "bt"):
			self.__destinationServer = ""
			self.__commandType = "begin"
			return "BT:" + self.__generateId()
		elif(words[0] == "R" or words[0] == "r"):
			if(len(words) == 2):
				self.__destinationServer = words[1]
				self.__commandType = "read"
				return "R:" + self.__generateId()
			else:
				self.__commandType = "invalid"
				return "invalid"
		elif(words[0] == "W" or words[0] == "w"):
			if(len(words) == 3):
				self.__destinationServer = words[1]
				self.__commandType = "write"
				return "W:" + self.__generateId() + ":" + words[2]
			else:
				self.__commandType = "invalid"
				return "invalid"
		elif(words[0] == "C" or words[0] == "c"):
			self.__destinationServer = ""
			self.__commandType = "commit"
			return "C:" + self.__generateId()
		elif(words[0] == "A" or words[0] == "a"):
			self.__destinationServer = ""
			self.__commandType = "abort"
			return "A:" + self.__generateId()
		elif(words[0] == "ET" or words[0] == "et"):
			self.__destinationServer = ""
			self.__commandType = "end"
			return "ET"
		else:
			self.__commandType = "invalid"
			return "invalid"
	
	def getDestinationServer(self):
		self.__destinationServer = self.__destinationServer.rstrip()
		return self.__destinationServer
	
	def getCommandType(self):
		return self.__commandType
	
	def __generateId(self):
		#chars = string.ascii_uppercase + string.digits + string.ascii_lowercase + "!@#$%^&*()-=_+[]{};':?><,."
		#size = 16
		#return ''.join(random.choice(chars) for _ in range(size)),
		return "1111111111"