import sys
from Utils.Logger import Logger

from Server.ServerCore import ServerCore

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	Logger.initLogger()
	log = Logger.getLogger()
	
	if(len(argv) != 3):
		log.error("IP or port not specified!" "")
		return 1
		
	server = ServerCore()
	ip = argv[1]
	port = int(argv[2])
	server.start(ip, port)

if __name__ == '__main__':
	sys.exit(main())