import sys

sys.path.append('..')

import re

from Vertex import *
from Edge import *
from Util import *

"""
Finds the closest two vertices in a graph by euclidean distance
"""
def findClosestVerticesEuclidean(graph):
	a, b = None, None
	distance = 0xFFFFFFFF
	
	for v1 in graph.vertices:
		for v2 in graph.vertices:
			newdistance = vdistance(v1, v2)
			if(newdistance < distance):
				a, b = v1, v2
				distance = newdistance

	return a, b

"""
Finds the closest two vertices in a graph
"""
def findClosestVertices(graph):
	a, b = None, None
	distance = 0xFFFFFFFF

	for e in graph.edges:
		dis = e.length()
		if(dis < distance):
			a, b = e.getVertices()
			distance = dis
	return a, b

"""
Finds the closest vertex in a graph to an input vertex
"""
def findClosestVertexTo(graph, vertex):
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
Finds the closest vertex in a graph to an input vertex by euclidean distance
"""
def findClosestVertexToEuclidean(graph, vertex):
	a = None
	distance = 0xFFFFFFFF

	for v in graph.vertices:
		newdistance = vdistance(v1, vertex)
		if(newdistance < distance):
			a = v
			distance = newdistance

	return a

"""
Finds the closest vertex in a graph to an input vertex that is not in the vertexSet
"""
def findClosestVertexToNotIn(graph, vertex, vertexSet):
	a = None
	distance = 0xFFFFFFFF

	neighbors = graph.getNeighborEdges(vertex)

	if(neighbors == None):
		return None

	for edge in neighbors:
		if(edge.length() < distance):
			b, c = edge.getVertices()
			if(b == vertex):
				if(c in vertexSet):
					continue
				else:
					a = c
			else:
				if(b in vertexSet):
					continue
				else:
					a = b
			distance = edge.length()
	return a

def findClosestVerticesFromPartition(graph, vertexSetOne, vertexSetTwo):
	if not(graph.containsAllVertices(vertexSetOne) and graph.containsAllVertices(vertexSetTwo)):
		return None

	edges = graph.edges

	a, b = None, None
	distance = 0xFFFFFFFF
	
	for edge in edges:
		c, d = edge.getVertices()

		if not((c in vertexSetOne and d in vertexSetTwo) or (c in vertexSetTwo and d in vertexSetOne)):
			continue

		if(edge.length() < distance):
			a, b = c, d
			distance = edge.length()

	return a, b

class Graph(Component.Component):

	def __init__(self, vertices = None, edges = None, info = None):
		if(info != None):
			self.info = info
		else:
			self.info = GRAPH_INFO_UNDIRECTED | GRAPH_INFO_UNWEIGHTED # Default
		self.vertices = vertices
		self.edges = edges

	def createSubgraphFromVSet(self, vertexSet):
		pass

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

	def containsAllVertices(self, vertexSet):
		for v in vertexSet:
			if not v in self.vertices:
				return False

		return True

	def containsAllEdges(self, edgeSet):
		for e in edgeSet:
			if not e in self.edges:
				return False

		return True

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
