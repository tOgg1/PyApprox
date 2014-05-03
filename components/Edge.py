from Vertex import *
from Util import *

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


	def containsVertex(self, vertex):
		return vertices[0] == vertex or vertices[1] == vertex

	def setVertexOne(self, vertex):
		self.vertices[0] = vertex

	def setVertexTwo(self, vertex):
		self.vertices[1] = vertex

