from Utils.Logger import Logger
from Utils.ServerList import ServerList

class ClientCore(object):
	def __init__(self):
		self.__log = Logger.getLogger()
		self.__serverList = ServerList()
		self.__serverList.parseList()

	def start(self):
		# start logging
		self.__log.info("Starting client...")
		
		# TODO: parse file and get list of servers
		
		while(True):
			self.__printInfo()
			
	def __printInfo(self):
		print "POSSIBLE SERVERS:",
		for name in self.__serverList.getNames():
			print name,
		print 