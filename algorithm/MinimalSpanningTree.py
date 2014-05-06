from Graph import *

def createMinimalSpanningTree(graph):
	if not(isinstance(graph, Graph)):
		raise Exception("A minimal spanning tree can not be created for anything else than a graph")
	return graph #TODO