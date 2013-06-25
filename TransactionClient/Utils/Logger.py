import logging

class Logger(object):
	
	@staticmethod
	def initLogger():
		formatter = logging.Formatter("[%(levelname)s] %(message)s")
		
		consoleHandler = logging.StreamHandler()
		consoleHandler.setLevel(logging.DEBUG)
		consoleHandler.setFormatter(formatter)
		
		logger = logging.getLogger("ServerLogger")
		logger.setLevel(logging.DEBUG)
		logger.addHandler(consoleHandler)
	
	@staticmethod
	def getLogger():
		return logging.getLogger("ServerLogger")