import socket
from Utils.Logger import Logger
from Server.ThreadManager import ThreadManager

class ConnectionListener(object):

	def __init__(self):
		# create thread manager
		self.__threadManager = ThreadManager()
		
		# create a TCP/IP socket
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def listen(self, serverIP, serverPort):
		log = Logger.getLogger()

		# show given IP and port
		serverAddress = (serverIP, serverPort)
		log.info("Listening for TCP/IP on %s:%d", serverAddress[0], serverAddress[1])

		# bind the socket and listen
		self.__socket.bind(serverAddress)
		self.__socket.listen(1)

		while(True):
			log.debug("Waiting for connection...")
			connSocket, clientAddress = self.__socket.accept()
			try:
				log.debug("Client connected: %s:%d", clientAddress[0], clientAddress[1])
				while True:
					data = connSocket.recv(512)
					log.debug("Received '%s'", data)
					if data:
						self.__threadManager.createTransactionThread(clientAddress[0], clientAddress[1], data)
					else:
						break
			finally:
				connSocket.close()