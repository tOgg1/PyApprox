import Vertex

class Edge:

	def __init__(self, vertices, weight = None):
		self.vertices = vertices
		
		if not isinstance(vertices, tuple):
			raise Exception("Invalid arguments. Vertices needs to be a tuple with two vertices");


		if weight == None:
			weight = 1
		else:
			self.weight = weight

	def containsVertex(self, vertex):
		return vertices[0] == vertex or vertices[1] == vertex

