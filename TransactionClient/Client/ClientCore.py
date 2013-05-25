from subprocess import call
from ConnectionManager import ConnectionManager
from Utils.Logger import Logger
from Utils.ServerList import ServerList
from Utils.CommandParser import CommandParser

class ClientCore(object):
	def __init__(self):
		self.__log = Logger.getLogger()
		self.__servers = ServerList()
		self.__servers.parseList()
		self.__commandParser = CommandParser()
		self.__connectionManager = ConnectionManager()

	def start(self):
		# start logging
		self.__log.info("Starting client...")
		
		# user command loop
		while(True):
			call(["clear"])
			self.__printInfo()
			userCommand = raw_input()
			
			# parse user command, get destination server
			serverCommand = self.__commandParser.parse(userCommand)
			destinationServer = self.__commandParser.getDestinationServer()
			
			# send command
			response = ""
			if(destinationServer == ""):
				for name in self.__servers.getNames():
					response = self.__connectionManager.sendCommand(name, serverCommand)
					self.__printOutput("[" + name + "]: " + response)
			else:
				response = self.__connectionManager.sendCommand(destinationServer, serverCommand)
				self.__printOutput("[" + destinationServer + "]: " + response)

			print
			raw_input()
			
	def __printInfo(self):
		# list all registered servers
		print "POSSIBLE SERVERS:",
		for name in self.__servers.getNames():
			print name,
		print
		
		print "COMMANDS:"
		print "1) BT			- begin transaction"
		print "2) R:<id>		- read resource from server <id>"
		print "3) W:<id>:<data>	- write <data> to reasource on server <id>"
		print "4) C			- commit transaction"
		print "5) A			- abort transaction"
		print "6) ET			- end transaction"
		print "\n<<<",
		
	def __printOutput(self, data):
		print ">>>", data
