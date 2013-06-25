import string
import random
from subprocess import call
from TransactionManager import TransactionManager
from Utils.Logger import Logger
from Utils.ServerList import ServerList
from Utils.CommandParser import CommandParser

class ClientCore(object):
	def __init__(self):
		self.__log = Logger.getLogger()
		self.__servers = ServerList()
		self.__servers.parseList()
		self.__commandParser = CommandParser()
		self.__transacationId = str(self.__generateId())
		self.__transactionManager = TransactionManager(self.__transacationId)

	def start(self):
		# start logging
		self.__log.info("Starting client...")
		
		# user command loop
		while(True):
			call(["clear"])
			self.__printInfo()
			userCommand = raw_input()
			
			# parse user command, get destination server
			serverCommand = self.__commandParser.parse(userCommand, self.__transacationId)
			destinationServer = self.__commandParser.getDestinationServer()
			commandType = self.__commandParser.getCommandType()
			
			# process command
			self.__transactionManager.processCommand(commandType, destinationServer, serverCommand)

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
		print "\n<<<",
	
	def __generateId(self):
		chars = string.ascii_uppercase + string.digits + string.ascii_lowercase + "!@#$%^&*()-=_+[]{};':?><,."
		size = 16
		return ''.join(random.choice(chars) for _ in range(size)),