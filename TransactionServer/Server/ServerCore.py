from Utils.Logger import Logger
from Transactions.WALRegister import WALRegister

class ServerCore(object):
	
	def __init__(self):
		return

	def start(self, port = 10000):
		# start logging
		log = Logger.getLogger()
		log.info("Starting server...")
		
		# prepare WAL register (nothing happens if WAL is already initialized
		walReg = WALRegister()
		initWALStat = walReg.initWAL()
		if(initWALStat == False):
			log.error("Initializing WAL register failed! Shutting down server...")
			return
		
		# check WAL registry consistency
		unfinishedTtransactions = walReg.checkConsistency()
		if(len(unfinishedTtransactions) > 0):
			# TODO: some transactions are unfinished, abort them
			for t in unfinishedTtransactions:
				
	
	def initWAL(self):
		return True