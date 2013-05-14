from TransactionStorage import TransactionStorage
from WALRegister import WALRegister

class TransactioManager(object):
	
	def beginTransaction(self, transactionIP, transactionPort):
		# register transaction
		transStorage = TransactionStorage()
		transId = transStorage.add(transactionIP, transactionPort)
		
		# log BT in WAL register
		walReg = WALRegister()
		walReg.logBegin(transId)
	
	def endTransaction(self, transactionId):
		return