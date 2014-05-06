import sys

sys.path.append('components')
sys.path.append('algorithm')
sys.path.append('util')

from Element import *
from Vertex import *
from Set import *
from Parser import *
from Graph import *

from TravellingSalesman import *

def main():
	printDebugGraph(loadAndSolveTSP("res/graph_one.algdata"))

def testLoad():
	graph = loadGraph("res/graph_one.algdata")

	print "VerteCount:", graph.vertexCount()
	print "EdgeCount:", graph.edgeCount()
	print "IsWeighted, isUnweighted: ", graph.isWeighted(), graph.isUnweighted()
	print "IsDirected, isUndirected: ", graph.isDirected(), graph.isUndirected()
	print "IsMetric:", graph.isMetric()
	print "IsColored:", graph.isColored()

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