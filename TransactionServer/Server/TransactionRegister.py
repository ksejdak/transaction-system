class TransactionRegister(object):
	
	def add(self, transactionIP, transactionPort):
		return transactionIP + ":" + str(transactionPort)
	
	def remove(self, transactionId):
		return
	
	def getIP(self, transactionId):
		return ""
	
	def getPort(self, transactionId):
		return -1