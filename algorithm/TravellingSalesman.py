from Graph import * 
from EulerPath import *
from MinimalSpanningTree import *

def loadAndSolveTSP(filename):
	graph = loadGraph(filename)
	return solveTravellingSalesman(graph)

def solveTravellingSalesman(graph):

	if not(isinstance(graph, Graph)):
		raise Exception("Traveling Salesman can not be solved with something other than a graph. I feel like this should be fairly obvious...")

	if not(graph.isMetric()):
		raise Exception("I like your audacity: Solving travelling salesman without a metric graph. However, I dont have the next 3000 years available.")

	mst = createMinimalSpanningTree(graph)
	return createEulerPath(mst)
