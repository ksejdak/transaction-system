import os
import sqlite3
from Utils.Settings import RESOURCE_PATH, SERVER_DB_FILE
from Utils.Logger import Logger

class WALRegister(object):

	def __init__(self):
		self.__dbName = RESOURCE_PATH + SERVER_DB_FILE
		self.__log = Logger.getLogger()

		# check if database file exists
		if(os.path.exists(self.__dbName) == False):
			self.__log.debug("DB file doesn't exists, creating...")
		
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		
		# check if WAL table exists within database
		c = dbConnection.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS WALRegister (id VARCHAR(20), command VARCHAR(5), before VARCHAR(200), after VARCHAR(200))")
		
		dbConnection.close()
	
	def checkConsistency(self):
		# TODO: check if all transactions are finished
		return
	
	def logBegin(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		  # @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "BT", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?)", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logEnd(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		  # @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "ET", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?)", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logWrite(self, transactionId, oldData, newData):
		dbConnection = sqlite3.connect(self.__dbName)		  # @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "W", oldData, newData)
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?)", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logCommit(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		  # @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "C", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?)", values)
		dbConnection.commit()
		dbConnection.close()
	
	def logAbort(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)		  # @UndefinedVariable
		c = dbConnection.cursor()
		values = (transactionId, "A", "", "")
		c.execute("INSERT INTO WALRegister VALUES (?, ?, ?, ?)", values)
		dbConnection.commit()
		dbConnection.close()