import sys

class Node:
	def __init__(self, id):
		self.id = id
		self.shortcuts = []
		self.succ_ = None
		self.nextSucc_ = None
		self.values = []

	def addShortcut(self, node):
		self.shortcuts.append(node)
	def appointSucc(self, node):
		self.succ_ = node
	def appointNextSucc(self, node):
		self.nextSucc_ = node
	def updateValues(self, values_):
		self.values.extend(values_)


# map of nodes
class DHT:
	def __init__(self, nodeList, shortCut_, upper, lower):
		self.map = {}
		self.upper = upper
		self.lower = lower
		self.fileRead = False
		self.buildRing(sorted(nodeList))
		self.buildShortcut(shortCut_)
		

	def buildRing(self, nodeList):

		#should be somewhere else, like the rest of this code
		#TODO:should raise exception instead of ignoring
		for node in nodeList:
			if(node > self.upper or node < self.lower):
				nodeList.remove(node)

		nodeList_ = nodeList*2
		nodes = [Node(i) for i in nodeList]
		helper = nodes*2
		for i in range(len(nodes)):
			nodes[i].appointSucc(helper[i+1])
			helper[i+1].updateValues(self.generateValues(nodeList_[i], nodeList_[i+1]))
			nodes[i].appointNextSucc(helper[i+2])
			self.map[nodeList[i]] = nodes[i]
			

	def generateValues(self, start, end):
		values = []
		#rint(f"start: {start}, end: {end}")
		if(start > end):
			values.extend([i for i in range(start+1, self.upper+1)])
			values.extend([i for i in range(self.lower, end)])
		else:
			values.extend([i for i in range(start+1, end+1)])
		#rint(values)
		return values

	def buildShortcut(self, shortCuts):
		helper = {}
		for elem in shortCuts:
			a = elem.split(":")
			key = int(a[0])
			value = int(a[1])
			if(key in helper):
				helper[key].append(value)
			else:
				helper[key] = [value]
		for key in helper:
			for values in helper[key]:
				self.map[key].addShortcut(self.map[values])
		self.fileRead = True

	def list(self):
		if(len(self.map) < 0):
			print("Nothing to list")
		else:
			for key in sorted(self.map.keys()):
				node_ = self.map[key]
				shortcuts_ = node_.shortcuts
				suc = node_.succ_
				nsucc = node_.nextSucc_
				print(f"{node_.id}:", end="")
				for s in shortcuts_:
					print(f"{s.id},",end="")

				print(f" S-{suc.id}, NS-{nsucc.id}")

	#omega bad, a is a list of possible shortcuts, b is comparison for successor
	def distance(self, a, look_key):
		best_val = a.succ_
		for s in a.shortcuts:
			if(s.id > a.succ_.id and s.id <= look_key):
				best_val = s
		return best_val

	def lookup(self, start, end):
		#lookup for a node containing a particular key. read document for more, got no idea
		weight = 0
		if(start == end):
			print(f"Result: Data stored in node {start} - {weight} requests sent")
		else:
			#naive without shortcuts
			current = self.map[start]
			while(end not in current.values):
				current = self.distance(current, end)
				weight += 1
			print(f"Result: Data stored in node {current.id} - {weight} requests sent")

	#again, very naive
	def join(self, key):
		#new node to join the ring
		if(key < self.lower or key > self.upper):
			print(f"Node index too large or too low. Bounds are: {self.lower} to {self.upper}")
		else:
			if(key not in self.map):
				self.map[key] = Node(key)
				helper = sorted(self.map.keys())*2
				index = 0
				for key in sorted(self.map.keys()):
					self.map[key].appointSucc(self.map[helper[index+1]])
					self.map[key].appointNextSucc(self.map[helper[index+2]])
					index += 1
			else:
				print("Node already in DHT")

	#naive omega+
	def leave(self, key):
		#remove node from ring
		if(len(self.map) <= 1):
			print("Cannot remove, list length at 1 or less")
		else:
			node_ = self.map.pop(key)
			helper = sorted(self.map.keys())*2
			index = 0
			for key_ in sorted(self.map.keys()):
				if(node_ in self.map[key_].shortcuts):
					self.map[key_].shortcuts.remove(node_)
				self.map[key_].appointSucc(self.map[helper[index+1]])
				self.map[key_].appointNextSucc(self.map[helper[index+2]])
				index += 1

	def shortcut(self, from_, to):
		if(from_ not in self.map or to not in self.map):
			print("No such node")
		else:
			#adds a shortcut from one node to another
			self.map[from_].addShortcut(self.map[to])

def main():
	upper, lower = None, None
	node_list = []
	shortCut_ = None
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
				shortCut_ = line.split(",")
				shortcutCheck = False
	#print(upper)
	#print(lower)
	#print(node_list)
	#print(shortCut_string)
	dht = DHT(node_list,shortCut_, upper, lower)
	dht.list()
	print("")
	dht.lookup(17, 69)
	print("")
	dht.join(7)
	dht.list()
	print("")
	dht.leave(5)
	dht.list()
	print("")
	dht.shortcut(7, 22)
	dht.list()
	

if __name__ == "__main__":
    main()