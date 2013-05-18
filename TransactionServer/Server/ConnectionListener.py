import socket
from TransactionRegister import TransactionRegister
from Transactions.TransactionThread import TransactionThread
from Utils.Logger import Logger

class ConnectionListener(object):

	def __init__(self, serverName):
		# create thread manager
		self.__serverName = serverName
		
		# create a TCP/IP socket
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def listen(self, serverIP, serverPort):
		log = Logger.getLogger()

		# show given IP and port
		serverAddress = (serverIP, serverPort)
		log.info("Server '%s' is listening for TCP/IP on %s:%d", self.__serverName, serverAddress[0], serverAddress[1])

		# bind the socket and listen
		try:
			self.__socket.bind(serverAddress)
			self.__socket.listen(1)
		except socket.error, e:
			log.error("Socket error: " + str(e))
			return

		while(True):
			log.info("Waiting for connection...")
			try:
				clientSocket, clientAddress = self.__socket.accept()
			except socket.error, e:
				log.error("Socket error: " + str(e))
				return
			
			log.info("Client connected: %s:%d", clientAddress[0], clientAddress[1])
			transactionRegister = TransactionRegister()
			transactionId = transactionRegister.add(clientAddress[0], clientAddress[1])
			thread = TransactionThread(self.__serverName, clientSocket, transactionId)
			thread.start()