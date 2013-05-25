from subprocess import call
from Utils.Logger import Logger
from Utils.ServerList import ServerList
from Utils.CommandParser import CommandParser

class ClientCore(object):
	def __init__(self):
		self.__log = Logger.getLogger()
		self.__serverList = ServerList()
		self.__serverList.parseList()
		self.__commandParser = CommandParser()

	def start(self):
		# start logging
		self.__log.info("Starting client...")
		
		# user command loop
		while(True):
			call(["clear"])
			self.__printInfo()
			command = raw_input()
			message = self.__commandParser.parse(command)
			self.__printOutput(message)
			print
			raw_input()
			
	def __printInfo(self):
		# list all registered servers
		print "POSSIBLE SERVERS:",
		for name in self.__serverList.getNames():
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
