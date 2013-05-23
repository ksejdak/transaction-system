import sys
from Utils.Logger import Logger

from Client.ClientCore import ClientCore

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	Logger.initLogger()
	
	client = ClientCore()
	client.start()

if __name__ == '__main__':
	sys.exit(main())