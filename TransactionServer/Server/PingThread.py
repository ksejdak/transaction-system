import time
from threading import Thread
from Network.PingTester import PingTester

class PingThread(Thread):
	
	def __init__(self, name):
		self.__name = name
	
	def run(self):
		pingTester = PingTester()
		while(True):
			pingTester.ping()
			time.sleep(1)