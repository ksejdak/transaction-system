from Utils.Logger import Logger

class ServerCore(object):
	
	def __init__(self):
		return

	def start(self, port = 10000):
		log = Logger.getLogger()
		log.info("Starting server...")
		return