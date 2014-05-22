import sys

sys.path.append('..')

import re

from Vertex import *
from Edge import *
from Util import *

"""
Finds the closest two nodes in a graph
"""
def findClosestNodesEuclidean(graph):
	a, b = None, None
	distance = 0xFFFFFFFF
	
	for v1 in graph.vertices:
		for v2 in graph.vertices:
			newdistance = vdistance(v1, v2)
			if(newdistance < distance):
				a, b = v1, v2
				distance = newdistance

	return a, b

def findClosestNodes(graph):
	a, b = None, None
	distance = 0xFFFFFFFF

	for e in graph.edges:
		dis = e.length()
		if(dis < distance):
			a, b = e.getVertices()
			distance = dis
	return a, b

def findClosestNodeTo(graph, vertex):
	a = None
	distance = 0xFFFFFFFF

	neighbors = graph.getNeighborEdges(vertex)

	if(neighbors == None):
		return None

	for edge in neighbors:
		if(edge.length() < distance):
			b, c = edge.getVertices()
			a = (c if a != c else b)
			distance = edge.length()
	return a

	
"""
Finds the closest node in a graph to an input node 
"""
def findClosestNodeToEuclidean(graph, vertex):
	a = None
	distance = 0xFFFFFFFF

	for v in graph.vertices:
		newdistance = vdistance(v1, vertex)
		if(newdistance < distance):
			a = v
			distance = newdistance

	return a

class Graph(Component.Component):

	def __init__(self, vertices = None, edges = None, info = None):
		if(info != None):
			self.info = info
		else:
			self.info = GRAPH_INFO_UNDIRECTED | GRAPH_INFO_UNWEIGHTED # Default
		self.vertices = vertices
		self.edges = edges

	def isWeighted(self):
		return bool(self.info & GRAPH_INFO_WEIGHTED)

	def isUnweighted(self):
		return bool(self.info & GRAPH_INFO_UNWEIGHTED)

	def isDirected(self):
		return bool(self.info & GRAPH_INFO_DIRECTED)

	def isUndirected(self):
		return bool(self.info & GRAPH_INFO_UNDIRECTED)

	def isMetric(self):
		return bool(self.info & GRAPH_INFO_METRIC)

	def isColored(self):
		return bool(self.info & GRAPH_INFO_COLORED) 

	def vertexCount(self):
		return len(self.vertices)

	def edgeCount(self):
		return 0 if self.edges == None else len(self.edges)

	def toString(self):
		ret = "Graph.properties = {\n";
		ret += "\tVertexCount:" + str(self.vertexCount()) + "\n"
		ret += "\tEdgeCount:" + str(self.edgeCount()) + "\n"
		ret += "\tIsWeighted, isUnweighted: " +  str(self.isWeighted()) +  str(self.isUnweighted()) + "\n"
		ret += "\tIsDirected, isUndirected: " + str(self.isDirected()) + str(self.isUndirected()) + "\n"
		ret += "\tIsMetric:" + str(self.isMetric()) + "\n"
		ret += "\tIsColored:" + str(self.isColored()) + "\n"
		ret += "}"

		if(self.vertices != None):
			ret += "\nGraph.vertices = {"
			for vertex in self.vertices:
				ret += "\n\t"+ vertex.toString()

		if(self.edges != None):
			ret += "\n}\nGraph.edges = {"
			for edge in self.edges:
				ret += "\n\t" + edge.toString()
			ret += "\n}"
		return ret

	def getNeighbors(self, vertex):
		if not(vertex in self.vertices):
			return None

		neighbors = []

		for edge in self.edges:
			if(edge.containsVertex(vertex)):
				a, b = edge.getVertices()

				if(a == vertex):
					neighbors.append(b)
				else:
					neighbors.append(a)
		return neighbors

	def getNeighborEdges(self, vertex):
		if not(vertex in self.vertices):
			return None

		neighbors = []

		for edge in self.edges:
			if(edge.containsVertex(vertex)):
				neighbors.append(edge)

		return neighbors
