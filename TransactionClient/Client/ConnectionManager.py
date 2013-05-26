import socket
from Utils.ServerList import ServerList
from Utils.Logger import Logger

class ConnectionManager(object):
	def __init__(self):
		self.__log = Logger.getLogger()
		self.__servers = ServerList()
		self.__servers.parseList()
		self.__sockets = {}
		
		for name in self.__servers.getNames():
			try:
				serverAddress = self.__servers.getAddress(name)
				
				# create a TCP/IP socket and connect to remote server
				serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				serverSocket.connect(serverAddress)
				
				# save socket
				self.__sockets[name] = serverSocket
			except socket.error, e:
				self.__log.error("Socket error: " + str(e))
				raise IOError

	def sendCommand(self, serverName, command):
		# get socket for given server
		serverSocket = self.__sockets[serverName]
		
		# send command to server
		serverSocket.send(command)
		response = serverSocket.recv(512)
		if(response == ""):
			self.__log.error("Server died or closed connection")
			raise IOError
			return ""
		else:
			return response