import sys

sys.path.append('components')
sys.path.append('algorithm')
sys.path.append('util')
sys.path.append('')

import random

from Element import *
from Vertex import *
from Set import *
from Parser import *
from Graph import *
from ParseSet import *
from ParseGraph import *

from TravellingSalesman import *
from KCenter import *

def main():
	testLoad()
	
def testKCenter():
	vertices = []

	for i in range(1, 1000):
		vertex = Vertex()
		vertex.pos.x = random.randint(-100, 100)
		vertex.pos.y = random.randint(-100, 100)
		vertices.append(vertex)

	kSet = solveKCenter(vertices, 10)
	graph = Graph(kSet) # For debugging
	print graph.toString()

def testLoad():
	graph = loadGraph("res/graph_one.algdata")

	print graph.toString()

	for v in graph.vertices:
		print v.toString()

	sets = loadSet("res/set_example.algdata")

	for set in sets: 
		usets = set.getSetElements()
		elements = set.getNonSetElements()
		for s in usets:
			print s
		for e in elements:
			print e

def printDebugGraph(graph):
	print graph.toString()

if __name__ == "__main__":
	main()