from Settings import RESOURCE_PATH

class FileWorker(object):
	
	def __init__(self, serverName):
		self.__file = RESOURCE_PATH + serverName
	
	def read(self):
		f = open(self.__file, "r")
		data = f.read()
		f.close()
		return data
	
	def write(self, data):
		f = open(self.__file, "w")
		f.write(data)
		f.close()
		return