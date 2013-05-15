from Utils.Logger import Logger
from Transactions.WALRegister import WALRegister
from Network.ConnectionListener import ConnectionListener

class ServerCore(object):

	def start(self, serverIP = "127.0.0.1", serverPort = 10000):
		# start logging
		log = Logger.getLogger()
		log.info("Starting server...")
		
		# prepare WAL register (nothing happens if WAL is already initialized
		walReg = WALRegister()
		initWALStat = walReg.initWAL()
		if(initWALStat == False):
			log.error("Initializing WAL register failed! Shutting down server...")
		
		# check WAL registry consistency
		#unfinishedTtransactions = walReg.checkConsistency()
		#if(len(unfinishedTtransactions) > 0):
			# TODO: some transactions are unfinished, abort them
		#	for t in unfinishedTtransactions:
		
		# start listening for incomming messages
		listener = ConnectionListener()
		listener.listen(serverIP, serverPort)