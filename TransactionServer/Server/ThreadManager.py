from PingThread import PingThread

class ThreadManager(object):

	def createPingThread(self, clientId):
		pingThread = PingThread(str(clientId))
		# register somewhere thread to kill it later
		pingThread.start()
	
	def createTransactionThread(self, clientIP, clientAddress, message):
		return