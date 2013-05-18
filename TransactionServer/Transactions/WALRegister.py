class WALRegister(object):

	def initWAL(self):
		# TODO: create DB if necessary
		return True
	
	def checkConsistency(self):
		# TODO: check if all transactions are finished
		return
	
	def logBegin(self, transactionId):
		return
	
	def logEnd(self, transactionId):
		return
	
	def logWrite(self, transactionId, oldData, newData):
		return
	
	def logCommit(self, transactionId):
		return
	
	def logAbort(self, transactionId):
		return
	