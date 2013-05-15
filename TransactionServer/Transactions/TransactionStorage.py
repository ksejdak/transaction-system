class TransactionStorage(object):
	
	def add(self, transactionIP, transactionPort):
		# TODO: return transactionId
		return -1
	
	def getId(self, transactionIP, transactionPort):
		return -1
	
	def getIP(self, transactionId):
		return ""
	
	def getPort(self, transactionId):
		return -1
	
	def remove(self, transactionId):
		return