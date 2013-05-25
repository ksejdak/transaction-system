import string
from Settings import RESOURCE_PATH
from Settings import SERVER_LIST_FILE

class ServerList(object):
	def __init__(self):
		self.__file = RESOURCE_PATH + SERVER_LIST_FILE
		self.__servers = {}

	def parseList(self):
		f = open(self.__file, "r")
		serverList = f.readlines()
		f.close()
		
		# parse server list
		for line in serverList:
			words = string.split(line, "	")
			serverName = words[0]
			serverIP = words[1]
			serverPort = words[2]
			self.__servers[serverName] = (serverIP, int(serverPort))
	
	def getNames(self):
		return self.__servers.keys()
	
	def getAddress(self, serverName):
		return self.__servers[serverName]