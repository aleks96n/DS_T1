import sys

def list():
	#list the nodes in the ring
	return
def lookup():
	#lookup for a node containing a particular key. read document for more, got no idea
	return

def join():
	#new node to join the ring
	return

def leave():
	#remove node from ring
	return

def shortcut():
	#adds a shortcut from one node to another
	return

def main():
	upper, lower = None, None
	node_list = []
	shortCut_string = None
	nodeCheck, keyCheck, shortcutCheck = False, False, False

	#very naive, but works
	with open(sys.argv[1], 'r') as f:
		for line in f:
			if(line.startswith("#k")):
				keyCheck = True
				continue
			elif(line.startswith("#n")):
				nodeCheck = True
				continue
			elif(line.startswith("#s")):
				shortcutCheck = True
				continue
			if(nodeCheck):
				helper = line.split(",")
				node_list.extend(int(i) for i in helper)
				nodeCheck = False
			elif(keyCheck):
				helper = line.split(",")
				upper, lower = int(helper[1]), int(helper[0])
				keyCheck = False
			elif(shortcutCheck):
				shortCut_string = line
				shortcutCheck = False
	print(upper)
	print(lower)
	print(node_list)
	print(shortCut_string)

	

if __name__ == "__main__":
    main()