
from Vertex import *
from Edge import *
from Parser import loadFile

def loadGraph(filePath):
	fileObject = loadFile(filePath)

	graph = Graph()

	for object in fileObject.objects:
		


class Graph:

	def __init__(self, vertices = None, Edges = None):
		self.vertices = vertices
		self.edges = edges

		#TODO: GEnerate edges from vertices if only one is given and vice versa
