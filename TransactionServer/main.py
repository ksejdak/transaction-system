import sys
from Utils.Logger import Logger

from Server.ServerCore import ServerCore

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	Logger.initLogger()
	log = Logger.getLogger()
	
	if(len(argv) != 2):
		log.error("Port not specified!" "")
		return 1
		
	server = ServerCore()
	port = int(argv[1])
	server.start(port)

if __name__ == '__main__':
	sys.exit(main())