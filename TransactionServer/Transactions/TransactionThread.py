from threading import Thread
import thread
from Utils.MessageParser import MessageParser
from Utils.Logger import Logger
from Utils.FileWorker import FileWorker
from WALRegister import WALRegister
from ResourceQueue import ResourceQueue

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
		self.__walRegister = WALRegister(self.__serverName)
		self.__resource = ResourceQueue()
		self.__resourceOwned = False
		
		# create functions mapping
		self.__handlers = {
			"begin": self.__begin,
			"end": self.__end,
			"read": self.__read,
			"write": self.__write,
			"commit": self.__commit,
			"globalCommit": self.__globalCommit,
			"abort": self.__abort,
			"invalid": self.__reject
		}
		
	def run(self):
		while(True):
			request = self.__socket.recv(512)
			if(request == ""):
				self.__log.info("Connection closed in thread [%s]", self.__name)
				self.__walRegister.emergeBYEncyAbort(self.__transactionId, True)
				self.__log.info("Exiting transaction thread [%s]", self.__name)
				thread.exit()

			requestType = self.__messageParser.parse(request)
			requestHandler = self.__handlers[requestType]
			requestHandler()
	
	def __begin(self):
		self.__log.debug("__begin called")
		
		# check if transaction is already started
		if(self.__walRegister.isStarted(self.__transactionId) == False):
			self.__walRegister.logBegin(self.__transactionId)
			self.__socket.send("HELLO")
		else:
			self.__sendERR()
	
	def __end(self):
		self.__log.debug("__end called")
		
		# check if transaction is started
		if(self.__walRegister.isStarted(self.__transactionId) == True):
			# check if transaction is commited
			if(self.__walRegister.isCommited(self.__transactionId) == False):
				self.__abort()

			self.__walRegister.logEnd(self.__transactionId)
			self.__socket.send("BYE:" + self.__transactionId)

		self.__socket.close()
		self.__log.info("Exiting transaction thread [%s]", self.__name)
		thread.exit()

	def __read(self):
		self.__log.debug("__read called")
		
		# check if transaction is started
		if(self.__walRegister.isStarted(self.__transactionId) == True):
			data = self.__file.read()
			self.__sendOK(data)
		else:
			self.__sendERR()
	
	def __write(self):
		self.__log.debug("__write called")
		
		# check if transaction is started
		if(self.__walRegister.isStarted(self.__transactionId) == True):
			# check if resource is already locked
			if(self.__resourceOwned == False):
				self.__log.debug("locking resource")
				# try to lock resource
				if(self.__resource.lock(self.__transactionId) == False):
					self.__socket.send("DEADLOCK DETECTED:" + self.__transactionId)
					return
				else:
					self.__log.debug("resource locked")
					self.__resourceOwned = True
	
			# write data
			newData = self.__messageParser.getData()
			oldData = self.__file.read()
			self.__walRegister.logWrite(self.__transactionId, oldData, newData)
			self.__file.write(newData)
			self.__sendOK()
		else:
			self.__sendERR()
	
	def __commit(self):
		self.__log.debug("__commit called")
		
		# check if transaction is started
		if(self.__walRegister.isStarted(self.__transactionId) == True):
			self.__sendOK()
		else:
			self.__sendERR()
	
	def __globalCommit(self):
		self.__log.debug("__globalCommit called")
		
		# check if transaction is started
		if(self.__walRegister.isStarted(self.__transactionId) == True):
			self.__walRegister.emergencyCommit(self.__transactionId)
			self.__walRegister.logCommit(self.__transactionId)
			# check if we had locked a resource
			if(self.__resourceOwned == True):
				self.__resource.unlock(self.__transactionId)
				self.__resourceOwned = False
				self.__log.debug("resource unlocked")

			self.__sendOK()
		else:
			self.__sendERR()
	
	def __abort(self):
		self.__log.debug("__abort called")
		
		# check if transaction is started
		if(self.__walRegister.isStarted(self.__transactionId) == True):
			self.__walRegister.emergencyAbort(self.__transactionId)
			self.__walRegister.logAbort(self.__transactionId)
			# check if we had locked a resource
			if(self.__resourceOwned == True):
				self.__resource.unlock(self.__transactionId)
				self.__resourceOwned = False
				self.__log.debug("resource unlocked")
			self.__sendOK()
		else:
			self.__sendERR()
	
	def __reject(self):
		self.__log.debug("__reject called")
		self.__log.debug("Invalid request: [%s]", self.__messageParser.getData())
		self.__sendERR("invalid request [" + self.__messageParser.getData() + "]")
	
	def __sendERR(self, msg = ""):
		if(msg == ""):
			self.__socket.send("ERR")
		else:
			self.__socket.send("ERR:" + msg)

	def __sendOK(self, msg = ""):
		if(msg == ""):
			self.__socket.send("OK")
		else:
			self.__socket.send("OK:" + msg)