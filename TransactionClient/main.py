import sys
from Utils.Logger import Logger

from Client.ClientCore import ClientCore

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	Logger.initLogger()
	log = Logger.getLogger()
	
	if(len(argv) != 4):
		log.error("IP, port or server name not specified!")
		log.info("usage: transction-client <IP> <Port> <Name>")
		return 1
		
	client = ClientCore()
	serverIP = argv[1]
	serverPort = int(argv[2])
	serverName = argv[3]
	client.start(serverIP, serverPort, serverName)

if __name__ == '__main__':
	sys.exit(main())