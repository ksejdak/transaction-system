from ConnectionManager import ConnectionManager
from Utils.ServerList import ServerList
from Utils.Logger import Logger

class TransactionManager(object):
	def __init__(self):
		self.__log = Logger.getLogger()
		self.__connectionManager = ConnectionManager()
		self.__servers = ServerList()
		self.__servers.parseList()
		
		# create functions mapping
		self.__handlers = {
			"begin": self.__begin,
			"end": self.__end,
			"read": self.__read,
			"write": self.__write,
			"commit": self.__commit,
			"globalCommit": self.__globalCommit,
			"abort": self.__abort
		}
		
	def processCommand(self, commandType, destinationServer, command):
		commandHandler = self.__handlers[commandType]
		commandHandler(destinationServer, command)
	
	def __begin(self, destinationServer, command):
		response = ""
		for name in self.__servers.getNames():
			response = self.__connectionManager.sendCommand(name, command)
			self.__printOutput("[" + name + "]: " + response)
	
	def __end(self, destinationServer, command):
		response = ""
		for name in self.__servers.getNames():
			response = self.__connectionManager.sendCommand(name, command)
			self.__printOutput("[" + name + "]: " + response)
	
	def __read(self, destinationServer, command):
		response = self.__connectionManager.sendCommand(destinationServer, command)
		self.__printOutput("[" + destinationServer + "]: " + response)
		
	def __write(self, destinationServer, command):
		response = self.__connectionManager.sendCommand(destinationServer, command)
		self.__printOutput("[" + destinationServer + "]: " + response)
		
	def __commit(self, destinationServer, command):
		# phase 1: send C to all known servers
		responseList = []
		for name in self.__servers.getNames():
			res = self.__connectionManager.sendCommand(name, command)
			responseList.append(res)
			
		# count positive replies, then send GC or A
		if(responseList.count("OK") == len(self.__servers.getNames())):
			self.__globalCommit("", "GC")
		else:
			self.__log.info("Two-phase commit failed, aborting...")
			self.__abort("", "A")
	
	def __globalCommit(self, destinationServer, command):
		# phase 2: send GC to all known servers
		response = ""
		for name in self.__servers.getNames():
			response = self.__connectionManager.sendCommand(name, command)
			self.__printOutput("[" + name + "]: " + response)
		
	def __abort(self, destinationServer, command):
		response = ""
		for name in self.__servers.getNames():
			response = self.__connectionManager.sendCommand(name, command)
			self.__printOutput("[" + name + "]: " + response)

	def __printOutput(self, data):
		print ">>>", data