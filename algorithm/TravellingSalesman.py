import copy

from Graph import * 
from EulerPath import *
from MinimalSpanningTree import *

def loadAndSolveTSP(filename):
	graph = loadGraph(filename)
	return solveTravellingSalesman(graph)

"""
Solve the travelling salesman problem with the double-tree algorithm.
RUNNING TIME: O(n^2)
APPROXIMATION: 2
"""
def solveTravellingSalesman(graph):

	if not(isinstance(graph, Graph)):
		raise Exception("Traveling Salesman can not be solved with something other than a graph. I feel like this should be fairly obvious...")

	if not(graph.isMetric()):
		raise Exception("I like your audacity; you want to solve travelling salesman without a metric graph. However, I dont have the next 3000 years available.")

	mst = createMinimalSpanningTree(graph)
	return createEulerPath(mst)

"""
Solve the travelling salesman problem with the christofedes algorithm.
RUNNING TIME: O(n^2)
APPROXIMATION: 3/2
"""
def solveTravellingSalesmanChristofedes(graph):
	pass

"""
Solve the travelling salesman problem with the nearest addition algorithm.
RUNNING TIME: O(n^2)
APPROXIMATION: 2
"""
def solveTravellingSalesmanNearestAddition(graph):

	if not(isinstance(graph, Graph)):
		raise Exception("Traveling Salesman can not be solved with something other than a graph. I feel like this should be fairly obvious...")

	if not(graph.isMetric()):
		raise Exception("I like your audacity; you want to solve travelling salesman without a metric graph. However, I dont have the next 3000 years available.")

	tspSet = []
	remaining = copy.copy(graph.vertices)

	a, b = findClosestVertices(graph)

	print "Nereast: ", a.toString(), b.toString()

	tspSet.append(a)
	tspSet.append(b)

	remaining.remove(a)
	remaining.remove(b)

	distance = 0

	while len(tspSet) < len(graph.vertices):
		a, b = findClosestVerticesFromPartition(graph, remaining, tspSet)

		if(a in remaining):
			i = tspSet.index(b)
			tspSet.insert(i+1, a)
			remaining.remove(a)
		else:
			i = tspSet.index(a)
			tspSet.insert(i+1, b)
			remaining.remove(b)
	return tspSet







