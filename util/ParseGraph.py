from Graph import *
from Graph import Graph as Graph
from Vertex import *
from Util import * 
from Parser import *

def loadGraph(filename):
	graphStructure = loadFile(filename)

	graph = Graph()

	infoObjects, scopeObjects = graphStructure.separate()

	info = 0

	for object in infoObjects:
		if not(object.name in legalGraphInfoData):
			raise Exception("Error while post-parsing graph data. Received an invalid info-object. Allowed infoobjects:".join(legalGraphInfoData))
		if not(object.flag in legalGraphInfoFlags[object.name]):
			raise Exception("Error while post-parsing graph data. Received an info-object with invalid type. Allowed types for infoclass ".join(legalGraphInfoFlags[object.name]))

		if(object.flag == "info"):
			info = info ^ parseFlags(object.values)

		if(object.flag == "type"):
			if not(object.values[0] == "graph"):
				raise Exception("Error while post-parsing graph data. meta:type was not set equal to graph")
			if not(len(object.values) == 1):
				raise Exception("Error while post-parsing graph data. meta::type had more than one value")

	if(info == 0):
		info = GRAPH_INFO_UNWEIGHTED | GRAPH_INFO_UNDIRECTED

	vertices = []
	edges = []

	currentEdgeId = 0
	for object in scopeObjects:
		
		if not(object.name in legalGraphScopes):
			raise Exception("Error while post-parsing graph data. Encountered illegal scopeobject: " + object.name)

		if(object.name == "data"):
			for underObject in object.values:
				if not(isinstance(underObject, Object)):
					raise Exception("Error while post-parsing graph data. Data-object had something else than an object as a child")

				if not(underObject.name in legalGraphScopes):
					raise Exception("Error while post-parsing graph data. Encountered illegal scopeobject: " + object.name)

				if(underObject.name == "vertices"):
					for element in underObject.values:
						if not (isinstance(element, Element)):
							raise Exception("Error while post-parsing graph data. Vertices-object had something else than an element as a child")
						
						if not (element.name in legalGraphElements[underObject.name]):
							raise Exception("Error while post-parsing graph data. Element type " + element.name +" is not legal in scopeobject " + underObject.name)
						
						vertex = parseVertex(element.values)
						duplicates = [x for x in vertices if x.id == vertex.id]
						if(len(duplicates) != 0):
							raise Exception("Error while post-parsing graph data. Duplicate vertices with id " + str(vertex.id))
						vertices.append(vertex)
						vertices = sorted(vertices, key=lambda x: x.id)

				if(underObject.name == "edges"):
					for element in underObject.values:
						if not (isinstance(element, Element)):
							raise Exception("Error while post-parsing graph data. Edges-object had something else than an element as a child")
					
						if not (element.name in legalGraphElements[underObject.name]):
							raise Exception("Error while post-parsing graph data. Element type " + element.name + " is not legal in scopeobject " + underObject.name)	

						edge = parseEdge(element.values, currentEdgeId, vertices)
						edges.append(edge)
						currentEdgeId += 1
		else:
			raise Exception("Error while post-parsing graph data. All data in a graph has to be put in a data-scopeobject")
	graph = Graph(vertices, edges, info)
	return graph

def parseFlags(infoValues):
	flag = 0

	if("weighted" in infoValues and "unweighted" in infoValues):
		raise Exception("Error while post-parsing graph data. The graph has been flagged as both weighted and unweighted")

	if("directed" in infoValues and "undirected" in infoValues):
		raise Exception("Error while post-parsing graph data. The graph has been flagged as both directed and undirected")

	if("weighted" in infoValues):
		flag |= GRAPH_INFO_WEIGHTED

	if("unweighted" in infoValues):
		flag |= GRAPH_INFO_UNWEIGHTED

	if("directed" in infoValues):
		flag |= GRAPH_INFO_DIRECTED

	if("undirected" in infoValues):
		flag |= GRAPH_INFO_UNDIRECTED

	if("metric" in infoValues):
		flag |= GRAPH_INFO_METRIC

	return flag

def parseVertex(vertexData):
	if(len(vertexData) > len(vertexElementOrder)):
		raise Exception("Error while post-parsing graph data. Invalid argument count for element `vertex`, expected expected 1-"+str(len(vertexElementOrder))+", got " + str(len(vertexData)))

	id = 0
	weight = 1
	pos = Position()
	color = "none"
	for i in range(len(vertexData)):
		splitData = vertexData[i].split("=")
		value = ""
		name = ""

		if(len(splitData) <= 1):
			name = vertexElementOrder[i] 
			value = splitData[0]
		else:
			name = splitData[0].replace(" ", "")
			value = splitData[1]

		value = value.replace(" ", "")

		if(idPattern.match(name)):
			id = int(value)
		elif(weightPattern.match(name)):
			weight = float(value)
		elif(positionPattern.match(name)):
			extracted = re.sub("[)]?[(]? ?", "", value).split(",")
			pos.x = float(extracted[0])
			pos.y = float(extracted[1])
		elif(colorPattern.match(name)):
			color = value

	v = Vertex()
	v.id = id
	v.color = getColor(color)
	v.pos = pos
	v.weight = weight

	return v

def parseEdge(edgeData, id, vertices):
	if(len(edgeData) > len(edgeElementOrder)):
		raise Exception("Error while post-parsing graph data. Invalid argument count for element `edge`, expected 1-"+str(len(edgeElementOrder))+", got " + str(len(edgeData)))

	v1 = None
	v2 = None
	weight = 1
	color = "none"

	for i in range(len(edgeData)):
		splitData = edgeData[i].split("=")
		value = ""
		name = ""

		if(len(splitData) <= 1):
			name = edgeElementOrder[i] 
			value = splitData[0]
		else:
			name = splitData[0].replace(" ", "")
			value = splitData[1]
		
		value = value.replace(" ", "")

		if(v1Pattern.match(name)):
			vid = int(value)
			v1 = vertices[vid-1]
		elif(v2Pattern.match(name)):
			vid = int(value)
			v2 = vertices[vid-1]
		elif(weightPattern.match(name)):
			weight = float(value)
		elif(colorPattern.match(name)):
			color = value

	if(v1 == None):
		raise Exception("Error while post-parsing graph data. Edge missing vertex 1.")
	
	if(v2 == None):
		raise Exception("Error while post-parsing graph data. Edge missing vertex 2.")

	e = Edge()
	e.id = id
	e.vertices = (v1, v2)
	e.weight = weight
	e.color = getColor(color)
	
	return e