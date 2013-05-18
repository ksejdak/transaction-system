from threading import Thread
from Utils.MessageParser import MessageParser
from Utils.Logger import Logger

class TransactionThread(Thread):
	
	def __init__(self, serverName, socket, transactionId):
		super(TransactionThread, self).__init__()
		
		#self.__name = transactionId
		self.__log = Logger.getLogger()
		self.__log.debug("Creating transaction thread for id: [%s]", transactionId)
		
		self.__serverName = serverName
		self.__socket = socket
		self.__transactionId = transactionId
		self.__messageParser = MessageParser()
		
		# create functions mapping
		self.__handlers = {
			"begin": self.__begin,
			"end": self.__end,
			"read": self.__read,
			"write": self.__write,
			"commit": self.__commit,
			"abort": self.__abort,
			"invalid": self.__reject
		}
		
	def run(self):
		while(True):
			request = self.__socket.recv(512)
			requestType = self.__messageParser.parse(request)
			requestHandler = self.__handlers[requestType]
			requestHandler()
	
	def __begin(self):
		self.__log.debug("__begin called")
		self.__socket.send("HELLO:" + self.__transactionId)
	
	def __end(self):
		self.__log.debug("__end called")
		return
	
	def __read(self):
		self.__log.debug("__read called")
		return ""
	
	def __write(self):
		self.__log.debug("__write called")
		return
	
	def __commit(self):
		self.__log.debug("__commit called")
		return
	
	def __abort(self):
		self.__log.debug("__abort called")
		return
	
	def __reject(self):
		self.__log.debug("__reject called")
		self.__log.debug("Invalid request: [%s]", self.__messageParser.getData())
		self.__socket.send("ERROR: invalid request [" + self.__messageParser.getData() + "]")