class MessageParser(object):

	def __init__(self):
		self.__data = ""
	
	def parse(self, message):
		if(message[0] == "R" or message[0] == "r"):
			return "read"
		elif(message[0] == "W" or message[0] == "w"):
			# save string to be written to file
			self.__data = message[1:]
			return "write"
		elif(message[:2] == "BT" or message[:2] == "bt"):
			# save timestamp of the transaction
			self.__data = message[1:]
			return "begin"
		elif(message[:2] == "ET" or message[:2] == "et"):
			return "end"
		elif(message[0] == "C" or message[0] == "c"):
			return "commit"
		elif(message[0] == "A" or message[0] == "a"):
			return "abort"
		else:
			self.__data = message
			return "invalid"
	
	def getData(self):
		self.__data = self.__data.rstrip()
		return self.__data