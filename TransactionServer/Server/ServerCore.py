import logging

class ServerCore(object):
	
	def __init__(self):
		return

	def start(self, port = 10000):
		logger = logging.getLogger("server_logger")
		logger.info("Starting server...")
		return