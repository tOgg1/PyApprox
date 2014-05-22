from Vertex import *
import random
import copy

"""
Solves the k-center problem. Does this by starting with a random vertex, and iteratively adding the vertex furthest away from the 
"""
def solveKCenter(vertices, k, start = None):

	if not(isinstance(vertices, list)):
		raise Exception("Invalid input to solveKCenter, expected list of vertices")

	if(start == None):
		start = random.randint(0, len(vertices)-1)
	elif(not isinstance(start, int)) or (start < 0):
		raise Exception("Invalid input to solveKCenter, \"start\" variable must be a non-negative integer")

	vertices = copy.deepcopy(vertices)

	kSet = []
	kSet.append(vertices[start])

	while(len(kSet) < k):
		kSet.append(findVertexFurthestFrom(vertices, kSet))

	return kSet

"""
Finds the vertex in vertexSet that is furthest away from kSet (by sum of radius-distances)
"""
def findVertexFurthestFrom(vertexSet, kSet):
	maximumDistance = 0
	curMaxVertex = None
	
	for vertex in vertexSet:
		distance = getAccumulativeDistance(vertex, kSet)
		
		if(distance > maximumDistance):
			curMaxVertex = vertex
			maximumDistance = distance
	return curMaxVertex

"""
Gets the accumulative distance from a vertex to all vertices in kSet
"""
def getAccumulativeDistance(vertex, kSet):
	dist = 0

	for kVertex in kSet:
		dist += vdistance(vertex, kVertex)

	return dist
