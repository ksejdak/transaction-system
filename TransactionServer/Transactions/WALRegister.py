import os
import sqlite3
from Utils.Settings import RESOURCE_PATH, SERVER_DB_FILE
from Utils.Logger import Logger
from Utils.FileWorker import FileWorker
from ResourceQueue import ResourceQueue

class WALRegister(object):

	def __init__(self, serverName):
		self.__dbName = RESOURCE_PATH + SERVER_DB_FILE
		self.__log = Logger.getLogger()
		self.__file = FileWorker(serverName)
		self.__resource = ResourceQueue()

		# check if database file exists
		if(os.path.exists(self.__dbName) == False):
			self.__log.debug("DB file doesn't exists, creating...")
		
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# check if WAL table exists within database
		c.execute("CREATE TABLE IF NOT EXISTS WALRegister (id VARCHAR(20), command VARCHAR(5), before VARCHAR(200), after VARCHAR(200), timestamp VARCHAR(20))")
		
		dbConnection.close()
	
	def checkConsistency(self):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# gather information about each transaction
		startedTransactions = []
		commitedTransactions = []
		writeTransactions = []
		finishedTransactions = []
		#transactionLogs = c.execute("SELECT * FROM WALRegister WHERE command <> 'W' ORDER BY timestamp DESC")
		transactionLogs = c.execute("SELECT * FROM WALRegister ORDER BY timestamp DESC")

		# check if there is any tranaction		
		if(c.rowcount is not None):
			for log in transactionLogs:
				# if this id is already in startedTransactions, it means that any other records with this id belong to other transaction
				if(log[0] in startedTransactions):
					continue
				
				if(log[1] == "BT"):
					if(log[0] not in startedTransactions):
						startedTransactions.append(log[0])
				elif(log[1] == "W"):
					if(log[0] not in writeTransactions):
						writeTransactions.append(log[0])
				elif(log[1] == "C"):
					if((log[0] not in commitedTransactions) and (log[0] not in writeTransactions)):
						commitedTransactions.append(log[0])
				elif(log[1] == "ET"):
					if(log[0] not in finishedTransactions):
						finishedTransactions.append(log[0])
			
			# check if all are finished
			toAbortTransactions = []
			toCommitTransactions = []
			for t in startedTransactions:
				if(t not in finishedTransactions):
					if(t in commitedTransactions):
						toCommitTransactions.append(t)
					else:
						toAbortTransactions.append(t)
			
			# repair WAL
			self.__repair(toAbortTransactions, toCommitTransactions)
		
		dbConnection.close()
	
	def emergencyAbort(self, transactionId, emergency = False):
		self.__log.debug("emergencyAbort called...")
		
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()

		# gather information about this transaction
		restoredValue = ""
		writeDone = False
		values = (transactionId,)
		for log in c.execute("SELECT * FROM WALRegister WHERE id = ? ORDER BY timestamp DESC", values):
			# if command is BT or C than we should stop, other data should be saved permanently
			if(log[1] == "BT" or log[1] == "C"):
				break
			
			# if command is W, check what was the previous value
			if(log[1] == "W"):
				writeDone = True
				restoredValue = log[2]
		
		# restore resource value
		if(writeDone == True):
			self.__file.write(restoredValue)
		
		# clean up if abort is forced after server crash
		dbConnection.close()
		if(emergency == True):
			self.logAbort(transactionId)
			self.logEnd(transactionId)
			self.__resource.unlock(transactionId)
			self.__log.debug("resource unlocked")
	
	def emergencyCommit(self, transactionId, emergency = False):
		self.__log.debug("emergencyCommit called...")

		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()

		# gather information about this transaction
		commitedValue = ""
		writeDone = False
		values = (transactionId,)
		for log in c.execute("SELECT * FROM WALRegister WHERE id = ? ORDER BY timestamp DESC", values):
			# if command is BT, then we should stop
			if(log[1] == "BT"):
				break
			
			# if command is C, we should skip it
			if(log[1] == "C"):
				continue
			
			# if command is W, check what was the modified value
			if(log[1] == "W"):
				writeDone = True
				commitedValue = log[3]
				break

		# restore resource value
		if(writeDone == True):
			self.__file.write(commitedValue)
		
		# clean up if commit is forced after server crash
		dbConnection.close()
		if(emergency == True):
			self.logEnd(transactionId)
			self.__resource.unlock(transactionId)

	def isStarted(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		started = False
		
		# gather information about this transaction
		values = (transactionId,)
		c.execute("SELECT * FROM WALRegister WHERE id = ? AND (command = 'BT' OR command = 'ET') ORDER BY timestamp DESC", values)
		log = c.fetchone()

		# check if there is any transaction
		if(log is None):
			return False
		
		if(log[1] == "BT"):
			started = True
		
		dbConnection.close()
		return started
	
	def isCommited(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		commited = True
		
		# gather information about this transaction
		values = (transactionId,)
		c.execute("SELECT * FROM WALRegister WHERE id = ? ORDER BY timestamp DESC", values)
		log = c.fetchone()
		
		if(log[1] == "W"):
			commited = False
		
		dbConnection.close()
		return commited

	
	def logBegin(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		# @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "BT", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?, DateTime('now'))", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logEnd(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		# @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "ET", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?, DateTime('now'))", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logWrite(self, transactionId, oldData, newData):
		dbConnection = sqlite3.connect(self.__dbName)		# @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "W", oldData, newData)
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?, DateTime('now'))", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logCommit(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		# @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "C", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?, DateTime('now'))", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logAbort(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		# @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "A", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?, DateTime('now'))", values)
		dbConnection.commit()
		dbConnection.close()

	def __repair(self, toAbortTransactions, toCommitTransactions):
		# abort transactions that were interrupted by some error
		for t in toAbortTransactions:
			self.emergencyAbort(t, True)
		
		# commit transactions that were commited by not finished
		for t in toCommitTransactions:
			self.emergencyCommit(t, True)