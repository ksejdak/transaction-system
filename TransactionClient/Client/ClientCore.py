from Utils.Logger import Logger

class ClientCore(object):

	def start(self, serverIP, serverPort, name):
		# start logging
		log = Logger.getLogger()
		log.info("Starting client...")