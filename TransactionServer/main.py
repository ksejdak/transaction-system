import sys
import logging

from Server.ServerCore import ServerCore

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	#logging.basicConfig(format = "[%(levelname)s] %(message)s", level=logging.DEBUG)
	logger = logging.getLogger("server_logger")
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter("[%(levelname)s] %(message)s")
	ch.setFormatter(formatter)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(ch)
	
	#if(len(argv) != 2):
	#	logger.error("Port not specified!" "")
	#	return 1
		
	server = ServerCore()
	#port = int(argv[1])
	#server.start(port)
	server.start()

if __name__ == '__main__':
	sys.exit(main())