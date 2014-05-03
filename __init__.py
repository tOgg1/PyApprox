import sys

sys.path.append('components')
sys.path.append('algorithm')
sys.path.append('util')

from Element import *
from Vertex import *
from Set import *
from Parser import *
from Graph import *

def main():
	graph = loadGraph("res/graph_one.algdata")

	print "VerteCount:", graph.vertexCount()
	print "EdgeCount:", graph.edgeCount()
	print "IsWeighted, isUnweighted: ", graph.isWeighted(), graph.isUnweighted()
	print "IsDirected, isUndirected: ", graph.isDirected(), graph.isUndirected()
	print "IsMetric:", graph.isMetric()
	print "IsColored:", graph.isColored()

	for v in graph.vertices:
		print v.toString()

if __name__ == "__main__":
	main()