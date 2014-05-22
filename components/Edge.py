from Vertex import *
from Util import *
import Component

class Edge(Component.Component):

	def __init__(self, vertices = None):
		if(vertices != None):
			if not isinstance(vertices, tuple):
				raise Exception("Invalid arguments. Vertices needs to be a tuple with two vertices");
			self.vertices = vertices
		else:
			self.vertices = ()

		self.weight = 1
		self.color = COLOR_NONE
		self.euclidean = True

	def containsVertex(self, vertex):
		return vertices[0] == vertex or vertices[1] == vertex

	def setVertexOne(self, vertex):
		self.vertices[0] = vertex

	def setVertexTwo(self, vertex):
		self.vertices[1] = vertex

	def toString(self):
		return "Edge = {vertex1 = " + str(self.vertices[0].id) + ", vertex2 = " + str(self.vertices[1].id) + ", weight = " + str(self.weight) + ", color = " + colorToString(self.color) + "}" 

	def length(self):
		return (vdistance(self.vertices[0], self.vertices[1]) if self.euclidean else self.weight)

	def getVertices(self):
		return self.vertices

