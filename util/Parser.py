import os
import re
import copy

OBJECT_SCOPED = 1
OBJECT_INFO = 2

class ParserObj:
	pass

class ObjectStructure(ParserObj):
	def __init__(self):
		self.objects = []

	def addObject(self, object):
		self.objects.append(object)

	def removeObject(self, object):
		self.objects.remove(object)

	def separate(self):
		scoped = []
		info = []

		for object in self.objects:
			if(object.type == OBJECT_SCOPED):
				scoped.append(object)
			else:
				info.append(object)

		return info, scoped

class Object(ParserObj):
	def __init__(self, name, flag):
		self.name = name
		self.flag = flag
		self.type = OBJECT_INFO # Default
		self.values = []

	def addValue(self, value):
		self.values.append(value)

class Element(ParserObj):
	def __init__(self, name):
		self.name = name
		self.values = []

	def addValue(self, value):
		self.values.append(value)

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
	patternInfo = re.compile("meta:(.*)$")

	metaObjects = []
	scopedObjects = []
	scopedObjectsStack = []
	scopedObject = None
	counter = 0

	# The files are parsed from the beginning to the end, never looking back
	for line in content:
		counter = counter+1

		# If we have an object
		if(patternObject.match(line)):
			myObject = parseObject(line)

			if(patternInfo.match(line)):
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
			if(scopedObject == None):
				raise Exception(lineDecl(filename, counter) + "Stray element discovered. Please make sure all elements are enclosed in a scoped object")
			element = parseElement(line)
			scopedObject.addValue(element)
			continue
		else:
			raise Exception(lineDecl(filename, counter)  +"Invalid symbol near " + line +". Line does not start with an element or object-declaration")

	for object in metaObjects:
		structure.addObject(object)

	for object in scopedObjects:
		structure.addObject(object)

	return structure

def parseElement(element):
	if not isinstance(element, basestring):
		raise Exception("Element passed in to parseElement was not a string, is it already parsed?")

	splitOne = element.replace("\t", "").split("=", 1)

	if(len(splitOne) == 0):
		raise Exception("Element did not have value, or name: " + element)

	name = splitOne[0].strip(" ")

	patternBracket = re.compile(" *[{](.*)[}] *")

	if not(patternBracket.match(splitOne[1])):
		raise Exception("Elements value was not correctly formatted: " + splitOne[1])

	if(len(patternBracket.findall(splitOne[1])) > 1):
		raise Exception("Elements")
	rawValues = splitOne[1].replace("{", "").replace("}", "")

	elm = Element(name)

	rawValuesArray = rawValues.split(",")

	temp = ""
	i = 0
	while i < len(rawValuesArray):
		try:
			# Parentheses can span several commas
			if("(" in rawValuesArray[i]):
				temp = rawValuesArray[i]
				while not(")" in rawValuesArray[i]):
					i = i+1
					temp += "," + rawValuesArray[i]
					if(i > len(rawValuesArray)-1):
						raise Exception("Element contained a value with an unclosed parantheses")
				elm.addValue(temp)
				temp = ""
				continue
			elm.addValue(rawValuesArray[i])
		finally:
				i = i+1			
	return elm

def parseObject(someObject):
	if not isinstance(someObject, basestring):
		raise Exception("Object was not passed in as a string, is it already parsed?")

	splitOne = someObject.split(":")

	if(len(splitOne) == 0):
		raise Exception("Invalid object passed into parseObject method. Expected \"objectname:objectflag( ?= ?(values)+)?, got: " + str(metaObject))

	splitTwo = splitOne[1].split("=", 1)

	for i in range(len(splitTwo)):
		splitTwo[i] = splitTwo[i].replace(" ", "").replace("\n", "")

	objectName = splitOne[0]
	objectFlag = splitTwo[0].replace(" ", "")

	object = Object(objectName, objectFlag)

	if(len(splitTwo) > 1):
		objectValues = splitTwo[1].replace(" ", "").split(",")
		for value in objectValues:
			object.addValue(value)
	else:
		object.type = OBJECT_SCOPED

	return object

def lineDecl(f, c):
	return str(f)+", "+str(c) +": "

