from TransactionStorage import TransactionStorage
from WALRegister import WALRegister
from Utils.FileWorker import FileWorker

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
	
	def read(self, transactionId):
		fileWorker = FileWorker()
		data = fileWorker.read()
		return data
	
	def write(self, data):
		fileWorker = FileWorker()
		fileWorker.write(data)
	