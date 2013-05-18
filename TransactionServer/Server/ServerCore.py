from Utils.Logger import Logger
from Transactions.WALRegister import WALRegister
from ConnectionListener import ConnectionListener

class ServerCore(object):

	def start(self, serverIP, serverPort, name):
		# start logging
		log = Logger.getLogger()
		log.info("Starting server...")
		
		# prepare WAL register (nothing happens if WAL is already initialized
		walRegister = WALRegister()
		initialized = walRegister.initWAL()
		if(initialized == False):
			log.error("Initializing WAL register failed! Shutting down server...")
		
		# check WAL register consistency
		walRegister.checkConsistency()
		
		# start listening for incomming messages
		listener = ConnectionListener(name)
		listener.listen(serverIP, serverPort)