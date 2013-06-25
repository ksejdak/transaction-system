import socket
from Transactions.TransactionThread import TransactionThread
from Utils.Logger import Logger

class ConnectionListener(object):

	def __init__(self, serverName):
		self.__log = Logger.getLogger()
		
		# create thread manager
		self.__serverName = serverName
		
		# create a TCP/IP socket
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def listen(self, serverIP, serverPort):
		# show given IP and port
		serverAddress = (serverIP, serverPort)
		self.__log.info("Server '%s' is listening for TCP/IP on %s:%d", self.__serverName, serverAddress[0], serverAddress[1])

		# bind the socket and listen
		try:
			self.__socket.bind(serverAddress)
			self.__socket.listen(1)
		except socket.error, e:
			self.__log.error("Socket error: " + str(e))
			return

		while(True):
			self.__log.info("Waiting for connection...")
			try:
				clientSocket, clientAddress = self.__socket.accept()
			except socket.error, e:
				self.__log.error("Socket error: " + str(e))
				return
			
			self.__log.info("Client connected: %s:%d", clientAddress[0], clientAddress[1])
			transactionId = clientAddress[0] + ":" + str(clientAddress[1])
			thread = TransactionThread(self.__serverName, clientSocket, transactionId)
			thread.start()