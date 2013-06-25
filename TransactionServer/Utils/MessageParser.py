import string

class MessageParser(object):

	def __init__(self):
		self.__data = ""
	
	def parse(self, message):
		message.rstrip()
		words = string.split(message, ":")
		
		if(words[0] == "BT" or words[0] == "bt"):
			return "begin"
		elif(words[0] == "R" or words[0] == "r"):
			return "read"
		elif(words[0] == "W" or words[0] == "w"):
			if(len(words) == 3):
				# save string to be written to file
				self.__data = words[2]
				return "write"
			else:
				return "invalid"
		elif(words[0] == "C" or words[0] == "c"):
			return "commit"
		elif(words[0] == "GC" or words[0] == "gc"):
			return "globalCommit"
		elif(words[0] == "A" or words[0] == "a"):
			return "abort"
		elif(words[0] == "ET" or words[0] == "et"):
			return "end"
		else:
			self.__data = message
			return "invalid"
	
	def getData(self):
		self.__data = self.__data.rstrip()
		return self.__data