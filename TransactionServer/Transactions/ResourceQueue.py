import os
import sqlite3
import time
from Utils.Settings import RESOURCE_PATH, SERVER_DB_FILE, DEADLOCK_TIMEOUT
from Utils.Logger import Logger

class ResourceQueue(object):
	
	def __init__(self):
		self.__dbName = RESOURCE_PATH + SERVER_DB_FILE
		self.__log = Logger.getLogger()

		# check if database file exists
		if(os.path.exists(self.__dbName) == False):
			self.__log.debug("DB file doesn't exists, creating...")
		
		dbConnection = sqlite3.connect(self.__dbName)	# @UndefinedVariable
		
		# check if ResourceQueue table exists within database
		c = dbConnection.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS ResourceQueue (id VARCHAR(20), timestamp VARCHAR(20))")
		
		dbConnection.close()
	
	def lock(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)	# @UndefinedVariable
		locked = False
		
		# insert transaction into queue indicating that it wants to lock the resource
		c = dbConnection.cursor()
		values = (transactionId,)
		c.execute("INSERT INTO ResourceQueue VALUES (?, DateTime('now'))", values)
		dbConnection.commit()
		
		# check if it is first in queue
		startTime = time.time()
		while(True):
			c.execute("SELECT * FROM ResourceQueue ORDER BY timestamp ASC")
			row = c.fetchone()
			if(transactionId in row):
				locked = True
				break
			else:
				# wait until resource is unlocked or timeout is reached
				time.sleep(1)
				if(time.time() - startTime >= DEADLOCK_TIMEOUT):
					self.__log.error("deadlock detected")
					values = (transactionId,)
					c.execute("DELETE FROM ResourceQueue WHERE id = ?", values)
					dbConnection.commit()
					break;
		
		dbConnection.close()
		return locked
	
	def unlock(self, transactionId):
		dbConnection = sqlite3.connect(self.__dbName)	# @UndefinedVariable
		
		# delete transaction from queue indicating that it wants to unlock the resource
		c = dbConnection.cursor()
		values = (transactionId,)
		c.execute("DELETE FROM ResourceQueue WHERE id = ?", values)
		dbConnection.commit()

		dbConnection.close()		