import os
import re
import copy

class ParserObj:
	pass

class ObjectStructure(ParserObj):
	def __init__(self):
		self.objects = []

	def addObject(self, object):
		self.objects.append(object)

	def removeObject(self, object):
		self.objects.remove(object)

class Object(ParserObj):
	def __init__(self, name, flag):
		self.name = name
		self.flag = flag
		self.values = []

	def addValue(self, value):
		self.values.append(value)

class Element(ParserObj):
	def __init__(self, name):
		self.name = name
		self.values = []

	def addValue(self, value):
		self.values.appned(value)

def loadFile(filename):
	if not os.path.isfile(filename):
		raise Exception("File does not exist: " + str(filename))
	file = open(filename, 'r')

	content = []

	# Load the lines into content, and do basic stripping of comments and whitespaces
	for line in file:
		line = line.strip(" ").strip("\t")
		if(len(line) != 0):
			if(line[0] == "#"):
				continue
			else:
				content.append(line)

	# Remove empty lines
	toberemoved = []
	patternEmpty = re.compile("^[\t?\n? ?]+")
	for line in content:
		if(patternEmpty.match(line)):
			toberemoved.append(line)

	for line in toberemoved:
		content.remove(line)

	# Remove comments at the end of lines
	patternComment = re.compile("[#](.*)$");
	newcontent = []
	for line in content:
		line = patternComment.sub(" ", line)
		newcontent.append(line)

	content = newcontent

	# Create objectstructure
	structure = ObjectStructure()

	patternObject = re.compile("^[a-zA-Z]+:[a-zA-Z]+( ?= ?([a-zA-Z]*,? ?)+)?$");
	patternElement = re.compile("^[a-zA-Z]+ ?=(.*)$") 
	patternScoped = re.compile("^[a-zA-Z]+:[a-zA-Z]+")
	patternMeta = re.compile("meta:(.*)$")
	patternData = re.compile("data:(.*)$")

	metaObjects = []
	scopedObjects = []
	scopedObjectsStack = []
	scopedObject = None
	counter = 0

	# The files are parsed from the beginning to the end
	for line in content:
		counter = counter+1

		# If we have an object
		if(patternObject.match(line)):
			myObject = parseObject(line)

			if(patternMeta.match(line)):
				metaObjects.append(myObject)
				continue
			# If we have a scoped-object
			elif(patternScoped.match(line)):
				if(myObject.flag == "start"):
					if(scopedObject != None):
						scopedObjectsStack.append(copy.copy(scopedObject))
					scopedObject = myObject
				elif(myObject.flag == "end"):
					if not(myObject.name == scopedObject.name):
						raise Exception(lineDecl(filename, counter) + "Reached end of invalid scope, near " + line + ". Expected " + scopedObject.name +", got " + myObject.name)

					# Is this the last element in the stack?
					if(len(scopedObjectsStack) == 0):
						scopedObjects.append(scopedObject)
						scopedObject = None
					# It is not, lets add our new object as a child of the first element in the stack
					else:
						object = scopedObjectsStack.pop()
						object.addValue(copy.copy(scopedObject))
						scopedObject = object
				else:
					raise Exception(lineDecl(filename, counter) + "A scoped object can only have flags \"start\" or \"end\": " + myObject.flag)
			else:
				raise Exception(lineDecl(filename, counter)  + "Invalid object declaration")
		# We have an element
		elif(patternElement.match(line)):
			if(scopedObject)
			element = parseElement(line)
			continue
		else:
			raise Exception(lineDecl(filename, counter)  +"Invalid symbol near " + line +". Line does not start with an element or object-declaration")

	for object in metaObjects:
		print object

	for object in scopedObjects:
		print object
	# # Debug
	# for line in content:
	# 	print line

def parseObject(metaObject):
	if not isinstance(metaObject, basestring):
		raise Exception("Object was not passed in as a string, is it already parsed?")

	splitOne = metaObject.split(":")

	if(len(splitOne) == 0):
		raise Exception("Invalid object passed into parseObject method. Expected \"objectname:objectflag( ?= ?(values)+)?, got: " + str(metaObject))

	splitTwo = splitOne[1].split("=")

	for i in range(len(splitTwo)):
		splitTwo[i] = splitTwo[i].strip(" ").strip("\n")

	objectName = splitOne[0]
	objectFlag = splitTwo[0].strip(" ")

	object = Object(objectName, objectFlag)

	if(len(splitTwo) > 1):
		objectValues = splitTwo[1].strip(" ").split(",")
		for value in objectValues:
			object.addValue(value)

	return object

def lineDecl(f, c):
	return str(f)+", "+str(c) +": "

loadFile("res/graph_one.algdata")
loadFile("res/set_example.algdata")
