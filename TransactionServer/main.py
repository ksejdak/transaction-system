import sys

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	print "argv = ", argv[0]

if __name__ == '__main__':
	sys.exit(main())