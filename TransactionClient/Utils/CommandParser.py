import string
import random

class CommandParser(object):

	def __init__(self):
		self.__destinationServer = ""
	
	def parse(self, message):
		words = string.split(message, ":")
		
		if(words[0] == "BT" or words[0] == "bt"):
			self.__destinationServer = ""
			return "BT:" + self.__generateId()
		elif(words[0] == "R" or words[0] == "r"):
			if(len(words) == 2):
				self.__destinationServer = words[1]
				return "R"
			else:
				return "invalid"
		elif(words[0] == "W" or words[0] == "w"):
			if(len(words) == 3):
				self.__destinationServer = words[1]
				return "W:" + words[2]
			else:
				return "invalid"
		elif(words[0] == "C" or words[0] == "c"):
			self.__destinationServer = ""
			return "C"
		elif(words[0] == "A" or words[0] == "a"):
			self.__destinationServer = ""
			return "A"
		elif(words[0] == "ET" or words[0] == "et"):
			self.__destinationServer = ""
			return "ET"
		else:
			return "invalid"
	
	def getDestinationServer(self):
		self.__destinationServer = self.__destinationServer.rstrip()
		return self.__destinationServer
	
	def __generateId(self):
		chars = string.ascii_uppercase + string.digits + string.ascii_lowercase + "!@#$%^&*()-=_+[]{};':?><,."
		size = 16
		return ''.join(random.choice(chars) for _ in range(size))