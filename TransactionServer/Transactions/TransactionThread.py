from threading import Thread
import thread
from Utils.MessageParser import MessageParser
from Utils.Logger import Logger
from Utils.FileWorker import FileWorker
from WALRegister import WALRegister

class TransactionThread(Thread):
	
	def __init__(self, serverName, socket, transactionId):
		super(TransactionThread, self).__init__()
		
		self.__name = transactionId
		self.__log = Logger.getLogger()
		self.__log.debug("Creating transaction thread [%s]", self.__name)
		
		self.__serverName = serverName
		self.__socket = socket
		self.__transactionId = transactionId
		self.__messageParser = MessageParser()
		self.__file = FileWorker(self.__serverName)
		self.__walRegister = WALRegister()
		
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
			if(request == ""):
				self.__log.info("Connection closed in thread [%s]", self.__name)
				self.__abort()
				self.__log.info("Exiting transaction thread [%s]", self.__name)
				thread.exit()

			requestType = self.__messageParser.parse(request)
			requestHandler = self.__handlers[requestType]
			requestHandler()
	
	def __begin(self):
		self.__log.debug("__begin called")
		self.__walRegister.logBegin(self.__transactionId)
		self.__socket.send("HELLO:" + self.__transactionId)
	
	def __end(self):
		self.__log.debug("__end called")
		self.__walRegister.logEnd(self.__transactionId)
		self.__socket.send("BYE:" + self.__transactionId)
		self.__log.info("Exiting transaction thread [%s]", self.__name)
		self.__socket.close()
		thread.exit()

	def __read(self):
		self.__log.debug("__read called")
		data = self.__file.read()
		self.__socket.send("READ:" + data)
	
	def __write(self):
		self.__log.debug("__write called")
		newData = self.__messageParser.getData()
		oldData = self.__file.read()
		self.__walRegister.logWrite(self.__transactionId, oldData, newData)
		self.__file.write(newData)
		self.__socket.send("WRITE:" + newData)
	
	def __commit(self):
		self.__log.debug("__commit called")
		self.__walRegister.logCommit(self.__transactionId)
		self.__socket.send("COMMIT:" + self.__transactionId)
	
	def __abort(self):
		self.__log.debug("__abort called")
		self.__walRegister.logAbort(self.__transactionId)
		self.__socket.send("ABORT:" + self.__transactionId)
	
	def __reject(self):
		self.__log.debug("__reject called")
		self.__log.debug("Invalid request: [%s]", self.__messageParser.getData())
		self.__socket.send("ERROR: invalid request [" + self.__messageParser.getData() + "]")